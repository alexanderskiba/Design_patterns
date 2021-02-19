from abc import ABC, abstractmethod

class AbstractEffect(Hero, ABC):
    """Общий абстрактный декоратор"""

    def __init__(self, base):
        self.base = base

    @abstractmethod
    def get_positive_effects(self):
        return self.positive_effects

    @abstractmethod
    def get_negative_effects(self):
        return self.negative_effects

    @abstractmethod
    def get_stats(self):
        pass

class AbstractNegative(AbstractEffect):
    """Абстрактный негативный декоратор"""
    def get_positive_effects(self):
        """Для отрицательных эффектов список положительных останется неизменным"""
        return self.base.get_positive_effects()

class AbstractPositive(AbstractEffect):
    """Абстрактный позитиный декоратор"""
    def get_negative_effects(self):
        """Для положительных эффектов список отрицательных останется неизменным"""
        return self.base.get_negative_effects()


class Berserk(AbstractPositive):
    """Декоратор берсерк
        Увеличивает характеристики: Сила, Выносливость, Ловкость, Удача на 7;
        уменьшает характеристики: Восприятие, Харизма, Интеллект на 3;
        количество единиц здоровья увеличивается на 50.
        """

    def get_stats(self):
        # Базовые характеристики
        stats = self.base.get_stats()
        stats["HP"] += 50
        stats["Strength"] += 7
        stats["Endurance"] += 7
        stats["Agility"] += 7
        stats["Luck"] += 7
        stats["Perception"] -= 3
        stats["Charisma"] -= 3
        stats["Intelligence"] -= 3
        return stats

    def get_positive_effects(self):
        return self.base.get_positive_effects() + [str(self)]

    def __str__(self):
        return "Berserk"

    def __repr__(self):
        return "Berserk"


class Blessing(AbstractPositive):
    """Декоратор благословение
        увеличивает все основные характеристики на 2.
        """

    def get_stats(self):
        # Базовые характеристики
        stats = self.base.get_stats()
        stats["Strength"] += 2
        stats["Endurance"] += 2
        stats["Agility"] += 2
        stats["Luck"] += 2
        stats["Perception"] += 2
        stats["Charisma"] += 2
        stats["Intelligence"] += 2
        return stats

    def get_positive_effects(self):
        return self.base.get_positive_effects() + [str(self)]

    def __str__(self):
        return "Blessing"

    def __repr__(self):
        return "Blessing"


class Weakness(AbstractNegative):
    """Декоратор слабость
        уменьшает характеристики: Сила, Выносливость, Ловкость на 4.
        """

    def get_stats(self):
        # Базовые характеристики
        stats = self.base.get_stats()
        stats["Strength"] -= 4
        stats["Endurance"] -= 4
        stats["Agility"] -= 4
        return stats

    def get_negative_effects(self):
        return self.base.get_negative_effects() + [str(self)]

    def __str__(self):
        return "Weakness"

    def __repr__(self):
        return "Weakness"


class EvilEye(AbstractNegative):
    """Декоратор сглаза
        уменьшает  характеристику Удача на 10.
        """

    def get_stats(self):
        stats = self.base.get_stats()
        stats["Luck"] -= 10
        return stats

    def get_negative_effects(self):
        return self.base.get_negative_effects() + [str(self)]

    def __str__(self):
        return "EvilEye"

    def __repr__(self):
        return "EvilEye"


class Curse(AbstractNegative):
    """Декоратор проклятья
        уменьшает все основные характеристики на 2.
        """

    def get_stats(self):
        # Базовые характеристики
        stats = self.base.get_stats()
        stats["Strength"] -= 2
        stats["Endurance"] -= 2
        stats["Agility"] -= 2
        stats["Luck"] -= 2
        stats["Perception"] -= 2
        stats["Charisma"] -= 2
        stats["Intelligence"] -= 2
        return stats

    def get_negative_effects(self):
        return self.base.get_negative_effects() + [str(self)]

    def __str__(self):
        return "Curse"

    def __repr__(self):
        return "Curse"


