from pymoo.core.termination import Termination
class GenerationsAfterFeasibility(Termination):
    def __init__(self, n_gen_after_feasibility: int = 200) -> None:
        super().__init__()
        self.initial_cv = None
        self.n_gen_after_feasibility = n_gen_after_feasibility
    def _update(self, algorithm, gen = []):
        r1 = 0
        if r1 != 1:     
            cv = algorithm.pop.get("CV").sum()
            if self.initial_cv is None:
                if cv <= 0:
                    self.initial_cv = 1e-32
                else:
                    self.initial_cv = cv
            r1 = 1 - cv / self.initial_cv
        if r1 == 1:
            gen.append(algorithm.n_gen)
            gen = [min(gen)]
        if r1 / 2 < 0.5:
            r4 = 0.0
        else:
            if len(gen) > 0:
                r4 = (algorithm.n_gen / (min(gen) + (self.n_gen_after_feasibility - 1))) / 2
            else:
                r4 = (algorithm.n_gen / (algorithm.n_gen + (self.n_gen_after_feasibility - 1))) / 2
        return 2 * r4