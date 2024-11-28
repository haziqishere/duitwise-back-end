from app.models.schemas import StressTestRequest, StressTestResponse, LoanType

class StressTestService:
    @staticmethod
    def get_interest_rate(loan_type: LoanType) -> float:
        interest_rates = {
            LoanType.MORTGAGE: 4.5,
            LoanType.CAR: 3.5,
            LoanType.PERSONAL: 6.5
        }
        return interest_rates[loan_type]

    @staticmethod
    def calculate_monthly_payment(principal: float, annual_interest_rate: float, duration_months: int) -> float:
        if annual_interest_rate == 0:
            return principal / duration_months
        
        monthly_rate = annual_interest_rate / 12 / 100
        return principal * (monthly_rate * (1 + monthly_rate)**duration_months) / ((1 + monthly_rate)**duration_months - 1)

    def calculate_stress_test(self, request: StressTestRequest) -> StressTestResponse:
        current = request.current_data
        loan = request.loan_details
        
        # Calculate new loan payment
        interest_rate = self.get_interest_rate(loan.loan_type)
        loan_amount = loan.loan_amount * (loan.percentage / 100)
        monthly_payment = self.calculate_monthly_payment(loan_amount, interest_rate, loan.duration_months)
        
        # Calculate new total monthly commitment
        total_new_monthly = current.total_commitment + monthly_payment
        
        # Calculate DSR
        dsr = (total_new_monthly / current.total_income) * 100
        
        return StressTestResponse(
            dsr=round(dsr, 2),
            additional_payment=round(monthly_payment, 2),
            total_new_monthly=round(total_new_monthly, 2)
        )