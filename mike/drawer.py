

class Drawer:

    def __init__(self):
        pass

    def move_to(x, y):
        # current position
        global X_POS, Y_POS
        # target position
        steps_x = x / LINEAR_STEP
        steps_y = y / LINEAR_STEP
        # delta
        delta_x = round(steps_x) - X_POS
        delta_y = round(steps_y) - Y_POS

        X_POS += delta_x
        Y_POS += delta_y

        # adjust for negative directions
        if delta_x < 0:
            delta_x = -delta_x
            x_dir = 1
        else:
            x_dir = 0
        if delta_y < 0:
            delta_y = -delta_y
            y_dir = 1
        else:
            y_dir = 0

        # Find the smoothest path by linking a series of steps together
        hgd = greatest_common_divisor(delta_x, delta_y)
        if hgd == 0:
            hgd = 1
        base = delta_x / hgd  # step in the x direction
        height = delta_y / hgd  # step in the y direction

        if base >= height:
            if base != 0:
                num_stairs = delta_x // base
            else:
                num_stairs = 1
            for _ in range(num_stairs):
                for _ in range(base):
                    step_motor("X", x_dir)
                    utime.sleep_us(STEP_DELAY)
                for _ in range(height):
                    step_motor("Y", y_dir)
                    utime.sleep_us(STEP_DELAY)
        elif base < height:
            if height != 0:
                num_stairs = 1
            else:
                num_stairs = delta_x // height
            for _ in range(num_stairs):
                for _ in range(base):
                    step_motor("X", x_dir)
                    utime.sleep_us(STEP_DELAY)
                for _ in range(height):
                    step_motor("Y", y_dir)
                    utime.sleep_us(STEP_DELAY)
