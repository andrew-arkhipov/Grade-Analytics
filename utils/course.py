class Course:
    @staticmethod
    def valid(link: str) -> bool:
        if link[32:37] == 'users':
            return False
        if link[-1].isdigit() and link[-7].isdigit():
            return True
        return False