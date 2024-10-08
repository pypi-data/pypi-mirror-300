class Entry:
    def __init__(self) -> None:
        self.e_type = self.set_type()
        self.e_sum = self.set_sum()

    def set_type(self, type_in: int = 0):
        self.e_type = type_in

    def set_sum(self, sum_in: float = 0.0):
        self.e_sum = sum_in
            
    def get_sum(self):
        return self.e_sum
            
    def __str__(self) -> str:
        tmp_sum = "{:.2f}".format(self.e_sum)
        return f"{'| Pajamos      |' if self.e_type == 1 else '| Išlaidos     |'} {tmp_sum}{' '*(10-len(str(tmp_sum)))}|"
