from dip import *

class CellCounting:
    def __init__(self):
        pass

    def blob_coloring(self, image):
        """Implement the blob coloring algorithm
        takes a input:
        image: binary image
        return: a list/dict of regions"""

        regions = dict()
        label = 1  

        height, width = shape(image)
        visited = zeros((height, width), dtype=bool)

        for x in range(width):  # Iterate over width first
            for y in range(height):  # Then iterate over height
                if image[y, x] == 255:
                    if not visited[y, x]:
                        stack = [(y, x)]
                        regions[label] = []
                        while stack:
                            cy, cx = stack.pop()
                            if 0 <= cy < height and 0 <= cx < width and image[cy, cx] == 255 and not visited[cy, cx]:
                                visited[cy, cx] = True
                                regions[label].append((cy, cx))
                                stack.extend([(cy + dy, cx + dx) for dy in [-1, 0, 1] for dx in [-1, 0, 1]])
                        label += 1

        return regions

    def compute_statistics(self, region):
        """Compute cell statistics area and location
        takes as input
        region: a list/dict of pixels in a region
        returns: region statistics"""

        stats = dict()

        for region_num, region_pixels in region.items():
            area = len(region_pixels)

            if area < 15:
                continue

            sum_y = sum(p[0] for p in region_pixels)
            sum_x = sum(p[1] for p in region_pixels)
            centroid_y = sum_y // area
            centroid_x = sum_x // area

            if centroid_y == 0 and centroid_x == 0:
                continue 

            stats[region_num] = {"area": area, "centroid": (centroid_y, centroid_x)}

        print(stats)
        return stats

    def mark_image_regions(self, image, stats):
        """Creates a new image with computed stats
        Make a copy of the image on which you can write text. 
        takes as input
        image: a list/dict of pixels in a region
        stats: stats regarding location and area
        returns: image marked with center and area"""

        height, width = image.shape

        marked_image = zeros((height, width, 3), dtype=uint8)

        for i in range(3):
            marked_image[:, :, i] = image  

        for region_num, region_stats in stats.items():
            centroid_y = int(region_stats['centroid'][0])
            centroid_x = int(region_stats['centroid'][1])

            putText(marked_image, "*", (centroid_x - 5, centroid_y + 5), FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

            text = f"{region_num}"
            text_area = f"{region_stats['area']}"
            putText(marked_image, text, (centroid_x - 5, centroid_y + 8), FONT_HERSHEY_SIMPLEX, 0.3, (255, 0, 0),1)
            putText(marked_image, text_area, (centroid_x - 5, centroid_y + 15), FONT_HERSHEY_SIMPLEX, 0.3, (0, 255, 0),1)

        return marked_image