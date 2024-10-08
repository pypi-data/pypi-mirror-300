from arturas_k_minibiudzetas.module.entry import Entry

class IncomeEntry(Entry):
    def __init__(self) -> None:
        super().__init__()  
        self.sender = ""
        self.additional_info = ""
        
    def set_info(self, sender, additional_info):
        self.sender = sender
        self.additional_info = additional_info
    
    def __str__(self) -> str:
        tmp_result = super().__str__()  
        tmp_string = f"{self.sender}, {self.additional_info}"
        return f"{tmp_result} {tmp_string}{' '*(30-len(str(tmp_string)))}|"