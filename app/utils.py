from datetime import timedelta


def calculate_camera_time_offset(PHONE_TIME: list, CAMERA_TIME: list) -> int:
    """Calculate offset for camera time

    Parameters
    ----------
    PHONE_TIME : list
        list with phone time
    PHONE_OFFSET : int
        offset for phone time
    CAMERA_TIME : int
        camera time

    Returns
    -------
    int
        offset for camera time
    """
    phone_delta_time = timedelta(
        hours=PHONE_TIME[0],
        minutes=PHONE_TIME[1],
        seconds=PHONE_TIME[2],
        milliseconds=PHONE_TIME[3] * 100,
    )
    camerta_delta_time = timedelta(
        hours=CAMERA_TIME[0],
        minutes=CAMERA_TIME[1],
        seconds=CAMERA_TIME[2],
    )
    # = phone_delta_time + timedelta(milliseconds=PHONE_OFFSET)
    return (phone_delta_time - camerta_delta_time).total_seconds() * 1000
