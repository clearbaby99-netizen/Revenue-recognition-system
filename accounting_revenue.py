from datetime import date

INVOICE_LOG = "invoice_log.txt"


class Contract:
    def __init__(self, project_name, client, contract_type):
        self.project_name = project_name
        self.client = client
        self.contract_type = contract_type

    def calculate_revenue(self):
        raise NotImplementedError("Subclasses must implement calculate_revenue()")

    def invoice_details(self):
        raise NotImplementedError("Subclasses must implement invoice_details()")


class FixedPriceContract(Contract):
    def __init__(self, project_name, client, total_price, percent_complete):
        super().__init__(project_name, client, "Fixed-Price")
        self.total_price = total_price
        self.percent_complete = percent_complete

    def calculate_revenue(self):
        return round(self.total_price * (self.percent_complete / 100), 2)

    def invoice_details(self):
        return (f"Fixed-Price Contract\n"
                f"Total Contract Value: ${self.total_price:,.2f}\n"
                f"Percent Complete: {self.percent_complete}%\n"
                f"Revenue Recognised: ${self.calculate_revenue():,.2f}")


class TimeAndMaterialsContract(Contract):
    def __init__(self, project_name, client, hours_worked, hourly_rate, materials_cost):
        super().__init__(project_name, client, "Time-and-Materials")
        self.hours_worked = hours_worked
        self.hourly_rate = hourly_rate
        self.materials_cost = materials_cost

    def calculate_revenue(self):
        return round((self.hours_worked * self.hourly_rate) + self.materials_cost, 2)

    def invoice_details(self):
        labour = self.hours_worked * self.hourly_rate
        return (f"Time-and-Materials Contract\n"
                f"Hours Worked: {self.hours_worked}\n"
                f"Hourly Rate: ${self.hourly_rate:,.2f}\n"
                f"Labour Charge: ${labour:,.2f}\n"
                f"Materials Cost: ${self.materials_cost:,.2f}\n"
                f"Revenue Recognised: ${self.calculate_revenue():,.2f}")


class CostPlusContract(Contract):
    def __init__(self, project_name, client, actual_cost, fee_percent):
        super().__init__(project_name, client, "Cost-Plus")
        self.actual_cost = actual_cost
        self.fee_percent = fee_percent

    def calculate_revenue(self):
        fee = self.actual_cost * (self.fee_percent / 100)
        return round(self.actual_cost + fee, 2)

    def invoice_details(self):
        fee = self.actual_cost * (self.fee_percent / 100)
        return (f"Cost-Plus Contract\n"
                f"Actual Cost Incurred: ${self.actual_cost:,.2f}\n"
                f"Fee: {self.fee_percent}% (${fee:,.2f})\n"
                f"Revenue Recognised: ${self.calculate_revenue():,.2f}")


def generate_invoice(contract, invoice_number):
    """Generate an invoice and append it to the invoice log file using the 'with' statement."""
    today = date.today().isoformat()
    invoice_text = (
        f"{'='*50}\n"
        f"INVOICE #{invoice_number}\n"
        f"Date: {today}\n"
        f"Client: {contract.client}\n"
        f"Project: {contract.project_name}\n"
        f"{'-'*50}\n"
        f"{contract.invoice_details()}\n"
        f"{'='*50}\n\n"
    )
    try:
        with open(INVOICE_LOG, "a") as file:
            file.write(invoice_text)
    except IOError as e:
        print(f"Error writing invoice: {e}")
        return None
    return invoice_text


def read_invoice_log():
    """Read back all invoices from the log file, handling the case where it doesn't exist yet."""
    try:
        with open(INVOICE_LOG, "r") as file:
            return file.read()
    except FileNotFoundError:
        return "No invoices have been generated yet."


def total_revenue_by_type(contracts):
    """Real-life question: total revenue recognised, broken down by contract type."""
    totals = {}
    for contract in contracts:
        totals[contract.contract_type] = totals.get(contract.contract_type, 0) + contract.calculate_revenue()
    return totals


if __name__ == "__main__":
    contracts = [
        FixedPriceContract("Office Website Redesign", "Clear99 Fintech", 15000, 60),
        TimeAndMaterialsContract("ERP Support Retainer", "Delta Corporation", 120, 45, 800),
        CostPlusContract("Warehouse Automation System", "Innscor Africa", 32000, 12),
    ]

    for i, contract in enumerate(contracts, start=1):
        invoice = generate_invoice(contract, invoice_number=1000 + i)
        print(invoice)

    print("Reading back the full invoice log from file:\n")
    print(read_invoice_log())

    print("Total revenue recognised by contract type:")
    for contract_type, total in total_revenue_by_type(contracts).items():
        print(f"  {contract_type}: ${total:,.2f}")
