from arturas_k_minibiudzetas.module.entry import Entry

class ExpensesEntry(Entry):
    def __init__(self) -> None:
        super().__init__()  
        self.payment_method = ""
        self.product_or_service = ""

    def set_info(self, payment_method, product_or_service):
        self.payment_method = payment_method
        self.product_or_service = product_or_service

    def __str__(self) -> str:
        tmp_result = super().__str__() 
        tmp_string = f"{self.payment_method}, {self.product_or_service}"
        return f"{tmp_result} {tmp_string}{' '*(max(0, 30-len(tmp_string)))}|"  
