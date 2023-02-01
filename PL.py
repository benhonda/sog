from random import randrange


def PLSimulation(min_cars_park: int, max_cars_park: int, max_cars_leaving: int, num_hours: int):

    waiting_to_park = 0
    car_arrival_rate = 0.0
    car_departure_rate = 0.0

    for hour in range(num_hours):
        print(f'hour: {hour + 1}')

        # cars arrive
        num_arrivals = randrange(min_cars_park, max_cars_park + 1)
        waiting_to_park += num_arrivals

        # update car_arrival_rate
        car_arrival_rate = (car_arrival_rate + num_arrivals) / 2

        # cars leave
        waiting_to_park = max(0, waiting_to_park - max_cars_leaving)

        # update car_departure_rate
        # car_departure_rate = (car_departure_rate + )

    print(f'After: {num_hours} hours...')
    print(f'Car arrival rate: {car_arrival_rate}')
    print(f'Car departure rate: {car_departure_rate}')
    print(f'Still waiting to park: {waiting_to_park}')


PLSimulation(min_cars_park=2, max_cars_park=5, max_cars_leaving=2, num_hours=6)
