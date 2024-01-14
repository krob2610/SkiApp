from datetime import timedelta


def calculate_camera_time_offset(
    PHONE_TIME: list, PHONE_OFFSET: int, CAMERA_TIME: list
) -> int:
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
        PHONE_TIME[0],
        PHONE_TIME[1],
        PHONE_TIME[2],
        PHONE_TIME[3],
    )
    camerta_delta_time = timedelta(
        CAMERA_TIME[0],
        CAMERA_TIME[1],
        CAMERA_TIME[2],
    )
    real_phone_time = phone_delta_time + timedelta(milliseconds=PHONE_OFFSET)
    return (real_phone_time - camerta_delta_time).total_seconds() * 1000
