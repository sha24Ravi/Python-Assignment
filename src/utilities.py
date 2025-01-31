



def paginate_data(networks,page):
    per_page = 5
    total_networks = len(networks)
    start = (page - 1) * per_page
    end = start + per_page

    # Slice the networks list for the current page
    paginated_networks = networks[start:end]

    return total_networks,paginated_networks
