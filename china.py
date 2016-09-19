import time


def initialize():
    storage.P = 0
    storage.H24 = 0
    storage.L24 = 0
    storage.S1 = 0
    storage.S2 = 0
    storage.R1 = 0
    storage.R2 = 0


def tick():
    PAIR = data.btc_usd

    H12 = data(interval=43200).btc_usd.warmup_period('high')
    L12 = data(interval=43200).btc_usd.warmup_period('low')
    C = data.btc_usd.warmup_period('close')

    if info.tick == 0:
        storage.P = C[-1]
        storage.S1 = C[-1]
        storage.S2 = C[-1]
        storage.R1 = C[-1]
        storage.R2 = C[-1]

    TIME = Decimal(info.current_time)

    JUNE1_7PM_UTC = Decimal(1401649200)

    DAY = Decimal(86400)

    DAYS = (TIME - JUNE1_7PM_UTC) / 86400

    if round(DAYS) == DAYS:
        storage.H24 = max(H12[-1], H12[-2])
        storage.L24 = min(L12[-1], L12[-2])
        storage.H24 = round(1000 * storage.H24) / 1000
        storage.L24 = round(1000 * storage.L24) / 1000
        storage.H24 = Decimal(storage.H24)
        storage.L24 = Decimal(storage.L24)

        storage.P = (storage.H24 + storage.L24 + Decimal(C[-1])) / Decimal(3)
        storage.P = round(1000 * storage.P) / 1000
        storage.P = Decimal(storage.P)

        storage.S1 = Decimal(2) * storage.P - storage.H24
        storage.S2 = storage.P - (storage.H24 - storage.L24)
        storage.R1 = Decimal(2) * storage.P - storage.L24
        storage.R2 = storage.P + (storage.H24 - storage.L24)

        log(DAYS)
        log(round(1000 * storage.P) / 1000)

    plot('P', storage.P)
    plot('S1', storage.S1)
    plot('S2', storage.S2)
    plot('R1', storage.R1)
    plot('R2', storage.R2)
