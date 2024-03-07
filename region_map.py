def get_region_code(project_zone_map, dep_datacenter, dep_region):
    try:
        datacenter_map = [dc for dc in project_zone_map if dc['name'] == dep_datacenter]
        if not datacenter_map:
            raise ValueError(f"Invalid datacenter: {dep_datacenter}")

        region_map = [rm for rm in datacenter_map[0]['values'] if rm['region'] == dep_region]
        if not region_map:
            raise ValueError(f"Invalid region: {dep_region}")

        region_code = datacenter_map[0]['region_continent'] + region_map[0]['region_sector']
        return region_code

    except Exception as e:
        print(f"Error in get_region_code: {e}")
        return None