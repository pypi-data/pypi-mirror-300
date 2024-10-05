import numpy as np
import pandas as pd
import torch


class Scout:
    """
    Explores a single path through the output space/tree.
    """

    def __init__(self, prompt, commander=None, t=0.5, t_aux=None, max_length=np.inf):
        self.prompt = prompt
        self.commander = commander
        self.max_length = max_length
        self.t = t
        self.t_aux = t_aux

        self._data = pd.DataFrame(columns=["token", "prob"])

    def get_data(self):
        out = {}
        out["phrase"] = "".join(self._data["token"].values)

        # Store metadata (temp, t_aux and max_length)
        out["temp"] = self.t
        out["temp_aux"] = self.t_aux
        out["max_length"] = self.max_length

        # Compute overall probability
        probs = self._data["prob"].values
        out["prob"] = np.prod(probs)

        # Compute normalized probabilities
        log_probs = np.log(probs)
        log_prob_sum = np.sum(log_probs)
        log_prob_sum_l = log_prob_sum / len(probs)
        prob_norm = np.exp(log_prob_sum_l)
        out["prob_norm"] = prob_norm

        return out

    def explore(self, verbose=False):
        prompt = self.prompt
        eos_token = self.commander.tokenizer.eos_token

        end_state = False
        while not end_state:

            # end_state is used to retrieve the last set of logits (inc. eos_token)
            if prompt.find(eos_token) >= 0 or self._data.shape[0] >= self.max_length:
                end_state = True

            self._step(prompt, end_state=end_state)
            prompt = self.prompt + "".join(self._data["token"].values)

            if verbose:
                print("DEBUG::", prompt)

    def _step(self, prompt, end_state=False, verbose=False):

        if self.commander.mode == "topk":
            logits_top, logits_top_idx = self.commander.get_top_k_logits(
                prompt, end_state=end_state, verbose=False
            )
        else:
            raise Exception("Modes other than topk not yet available")

        texts_top = self.commander.tokenizer.convert_ids_to_tokens(logits_top_idx)
        probs_top = torch.nn.functional.softmax(logits_top / self.t, dim=-1)

        if self.t_aux:
            probs_aux = torch.nn.functional.softmax(logits_top / self.t_aux, dim=-1)
            probs_aux = probs_aux.detach().numpy()

            if verbose:
                print("DEBUG::t_aux probs: ", probs_aux)

            next_idx = np.random.choice(len(texts_top), p=probs_aux)

        else:

            probs_top = probs_top.detach().numpy()
            # print('probs top detached', probs_top)
            next_idx = np.random.choice(len(texts_top), p=probs_top)

        # TODO: use pd.concat
        d = {"token": texts_top[next_idx], "prob": probs_top[next_idx].item()}
        self._data.loc[len(self._data)] = d
