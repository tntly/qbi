def build_ucsc_chromosome_location(chromosome_number:int, starting_base_pair:int, ending_base_pair:int):
    return f"chr{chromosome_number}:{starting_base_pair}-{ending_base_pair}"