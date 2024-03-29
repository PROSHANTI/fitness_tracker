from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Информационное сообщение о тренировке."""
    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    message: str = (
        'Тип тренировки: {training_type}; '
        'Длительность: {duration:.3f} ч.; '
        'Дистанция: {distance:.3f} км; '
        'Ср. скорость: {speed:.3f} км/ч; '
        'Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        """Получить главный вывод на экран."""
        return self.message.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: int = 1000
    M_IN_HOUR: int = 60

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError(f'Ты не заполнил функцию '
                                  f'"get_spent_calories" в'
                                  f' {Training.__name__}')

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__,
                           self.duration,
                           self.get_distance(),
                           self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""

    SPENT_CAL_1: float = 18
    SPENT_CAL_2: float = 1.79

    def get_spent_calories(self) -> float:
        """Получить калории."""
        return ((self.SPENT_CAL_1
                * self.get_mean_speed()
                + self.SPENT_CAL_2)
                * self.weight
                / self.M_IN_KM
                * self.duration
                * self.M_IN_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    SW_COEF_1: float = 0.035
    SW_COEF_2: float = 0.029
    KMH_IN_MSEC: float = 0.278
    CM_IN_M: int = 100

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: int) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        """Получить калории."""
        return ((self.SW_COEF_1 * self.weight + ((self.get_mean_speed()
                * self.KMH_IN_MSEC) ** 2 / (self.height / self.CM_IN_M))
            * self.SW_COEF_2
            * self.weight)
            * self.duration * self.M_IN_HOUR)


class Swimming(Training):
    """Тренировка: плавание."""

    # Коэффициенты для Swimming
    SWIM_COEF_1: float = 1.1
    SWIM_COEF_2: int = 2
    LEN_STEP: float = 1.38

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 length_pool: int,
                 count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return (self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration)

    def get_spent_calories(self) -> float:
        """Получить калории."""
        return ((self.get_mean_speed() + self.SWIM_COEF_1) * self.SWIM_COEF_2
                * self.weight * self.duration)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    work_type = {'SWM': Swimming,
                 'RUN': Running,
                 'WLK': SportsWalking}

    # Проверяем корректность типа тренировки
    correct_workout = work_type.get(workout_type)
    if not correct_workout:
        raise KeyError(f'Неверный тип тренировки: {workout_type}')
    return correct_workout(*data)


def main(training: Training) -> None:
    """Главная функция."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
