import math


class ASCVDFormulaExtended:
    def __init__(self, age, sex, race, systolic_bp, diastolic_bp, total_cholesterol, hdl_cholesterol, ldl_cholesterol,
                 diabetes, smoker, hypertension_treatment, statin, aspirin):
        self.age = age
        self.sex = sex
        self.race = race
        self.systolic_bp = systolic_bp
        self.diastolic_bp = diastolic_bp
        self.total_cholesterol = total_cholesterol
        self.hdl_cholesterol = hdl_cholesterol
        self.ldl_cholesterol = ldl_cholesterol
        self.diabetes = diabetes
        self.smoker = smoker
        self.hypertension_treatment = hypertension_treatment
        self.statin = statin
        self.aspirin = aspirin

        # Converting inputs into the required format
        self.is_female = sex == 'female'
        self.is_african = race == 'african_american'
        self.is_hypertension = hypertension_treatment

    # Optimal S010
    def s010(self):
        if self.is_african and self.is_female:
            return 0.95334
        elif not self.is_african and self.is_female:
            return 0.96652
        elif self.is_african and not self.is_female:
            return 0.89536
        else:
            return 0.91436

    # mnxb value
    def mnxb(self):
        if self.is_african and self.is_female:
            return 86.61
        elif not self.is_african and self.is_female:
            return -29.18
        elif self.is_african and not self.is_female:
            return 19.54
        else:
            return 61.18

    # Log transformations
    def ln_age(self):
        return math.log(self.age)

    def ln_hdl(self):
        return math.log(self.hdl_cholesterol)

    def ln_tot(self):
        return math.log(self.total_cholesterol)

    def tr_ln_sbp(self):
        return math.log(self.systolic_bp) * self.is_hypertension

    def nt_ln_sbp(self):
        return math.log(self.systolic_bp) * (not self.is_hypertension)

    def age2(self):
        return self.ln_age() * self.ln_age()

    def agetc(self):
        return self.ln_tot() * self.ln_age()

    def age_hdl(self):
        return self.ln_hdl() * self.ln_age()

    def agets_bp(self):
        return self.ln_age() * self.tr_ln_sbp()

    def agents_bp(self):
        return self.ln_age() * self.nt_ln_sbp()

    def agesmoke(self):
        return self.ln_age() * self.smoker

    def agedm(self):
        return self.ln_age() * self.diabetes

    def predict_calculate(self):
        if self.is_african and self.is_female:
            return (17.1141 * self.ln_age() + 0.9396 * self.ln_tot() - 18.9196 * self.ln_hdl() +
                    4.4748 * self.age_hdl() + 29.2907 * self.tr_ln_sbp() - 6.4321 * self.agets_bp() +
                    27.8197 * self.nt_ln_sbp() - 6.0873 * self.agents_bp() +
                    0.6908 * self.smoker + 0.8738 * self.diabetes)
        elif not self.is_african and self.is_female:
            return (-29.799 * self.ln_age() + 4.884 * self.age2() + 13.54 * self.ln_tot() -
                    3.114 * self.agetc() - 13.578 * self.ln_hdl() + 3.149 * self.age_hdl() +
                    2.019 * self.tr_ln_sbp() + 1.957 * self.nt_ln_sbp() + 7.574 * self.smoker -
                    1.665 * self.agesmoke() + 0.661 * self.diabetes)
        elif self.is_african and not self.is_female:
            return (2.469 * self.ln_age() + 0.302 * self.ln_tot() - 0.307 * self.ln_hdl() +
                    1.916 * self.tr_ln_sbp() + 1.809 * self.nt_ln_sbp() + 0.549 * self.smoker +
                    0.645 * self.diabetes)
        else:
            return (12.344 * self.ln_age() + 11.853 * self.ln_tot() - 2.664 * self.agetc() -
                    7.99 * self.ln_hdl() + 1.769 * self.age_hdl() + 1.797 * self.tr_ln_sbp() +
                    1.764 * self.nt_ln_sbp() + 7.837 * self.smoker - 1.795 * self.agesmoke() +
                    0.658 * self.diabetes)

    def cvd_predict(self):
        return 1 - math.pow(self.s010(), math.exp(self.predict_calculate() - self.mnxb()))

    def ten_year_risk(self):
        pred_value = self.cvd_predict()
        if pred_value != 1 and not math.isnan(pred_value):
            return f"{pred_value * 100:.1f}%"
        else:
            return "~%"


# Example usage with different inputs:
ascvd_calculator_test = ASCVDFormulaExtended(
    age=75, sex='male', race='other', systolic_bp=140, diastolic_bp=90,
    total_cholesterol=220, hdl_cholesterol=40, ldl_cholesterol=130, diabetes=True,
    smoker=True, hypertension_treatment=True, statin=False, aspirin=False)

print(ascvd_calculator_test.ten_year_risk())
