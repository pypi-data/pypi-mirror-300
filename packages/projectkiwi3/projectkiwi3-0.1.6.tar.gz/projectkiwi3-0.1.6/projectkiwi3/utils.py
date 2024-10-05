import numpy as np
from typing import List
import shapely

def normalizedPointsToLngLat(points: List[List[float]], taskCoordinates: List[List[float]], padding_factor: float = None) -> List[List[float]]:
    """Converts a list of points within a task to lat, lng coordinates. May be inaccurate for large tasks.

    Args:
        points (List[List[float]]): Input points in format: [[x, y], [x, y]], with x,y as normalised coordinates in range of [0,1]
        taskCoordinates (List[List[float]]): Coordinates for the task in [[lng, lat], [lng, lat]] format
        padding_factor(float, optional): If a padding factor was used to get the task image, it must be supplied here

    Returns:
        List[List[float]]: Coordinates for the polygon in [[lng, lat], [lng, lat]] format
    """
    
    if padding_factor:
        polygon = shapely.Polygon(taskCoordinates)
        scaled_polygon = shapely.affinity.scale(polygon, xfact=1+(2*padding_factor), yfact=1+(2*padding_factor))
        taskCoordinates = list(scaled_polygon.exterior.coords)

    x1_task = np.min(np.array(taskCoordinates)[:,0]).item() # most west
    x2_task = np.max(np.array(taskCoordinates)[:,0]).item() # most east
    y1_task = np.min(np.array(taskCoordinates)[:,1]).item() # most south
    y2_task = np.max(np.array(taskCoordinates)[:,1]).item() # most north

    outputPoints = []
    for p in points:
        p_lng_lat = [x1_task + p[0]*(x2_task-x1_task), y2_task - p[1]*(y2_task-y1_task)]
        outputPoints.append(p_lng_lat)
    return outputPoints


# x1, y1, x2, y2
def boxToLngLatPolygon(box: List[float], w, h, taskCoordinates: List[List[float]], padding_factor: float = None) -> List[List[float]]:
    """Converts a bounding box to a polygon with lng, lat coordinates

    Args:
        box (List[float]): Bounding box with x1, y1, x2, y2 format
        w (_type_): Image width in pixels
        h (_type_): Image height in pixels
        taskCoordinates (List[List[float]]): Coordinates for the task in [[lng, lat], [lng, lat]] format
        padding_factor(float, optional): If a padding factor was used to get the task image, it must be supplied here

    Returns:
        List[List[float]]: Coordinates for the polygon in [[lng, lat], [lng, lat]] format
    """    
    x1, y1, x2, y2 = box
    p1 = [x1/w, y1/h]
    p2 = [x2/w, y1/h]
    p3 = [x2/w, y2/h]
    p4 = [x1/w, y2/h]
    points = [p1, p2, p3, p4, p1]

    return normalizedPointsToLngLat(points, taskCoordinates, padding_factor)
    