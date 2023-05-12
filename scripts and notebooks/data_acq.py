import asyncio
import os
import httpx

from datetime import date

import geopandas as gpd

from params import *
from planet import order_request, Session, DataClient, data_filter, reporting


def create_requests(ht_aoi, tt_aoi, items):
    """Create order requests for the two sites."""
            
    ht_items = items[0]
    tt_items = items[1]

    ht_order = order_request.build_request(
        name='ht_order_' + str(datetime.today()),
        products=[order_request.product(item_ids=[i['id'] for i in ht_items],
                        product_bundle='analytic_sr_udm2',
                        item_type='PSScene')],
        tools=[order_request.clip_tool(aoi=ht_aoi.__geo_interface__['features'][0]['geometry']),
               order_request.harmonize_tool('Sentinel-2'),
               order_request.band_math_tool(b1="b1", b2="b2", b3="b3", b4="b4", b5="(b2-b4)/(b2+b4)", b6="(b4-b3)/(b4+b3)", pixel_type='32R')])
    
    tt_order = order_request.build_request(
        name='tt_order_' + str(datetime.today()),
        products=[order_request.product(item_ids=[i['id'] for i in tt_items],
                        product_bundle='analytic_sr_udm2',
                        item_type='PSScene')],
        tools=[order_request.clip_tool(aoi=tt_aoi.__geo_interface__['features'][0]['geometry']),
               order_request.harmonize_tool('Sentinel-2'),
               order_request.band_math_tool(b1="b1", b2="b2", b3="b3", b4="b4", b5="(b2-b4)/(b2+b4)", b6="(b4-b3)/(b4+b3)", pixel_type='32R')])
    
    return [ht_order, tt_order]


async def search_request(aoi_geom):
    """Search for images using parameters defined in params.py
    Returns list of found items for a given query."""

    item_type = ['PSScene']
    # Pull geometry from shapefile and create a data filter for the search
    geom_filter = data_filter.geometry_filter(aoi_geom.__geo_interface__['features'][0]['geometry'])
    clear_percent_filter = data_filter.range_filter('clear_percent', None, None, CLEAR_PERCENT)
    date_range_filter = data_filter.date_range_filter('acquired', TIME_RANGE_BEGINNING, TIME_RANGE_END)
    #visible_filter =  data_filter.range_filter('useful_data', None, None, VISIBLE_PERCENT)wwwww
    
    combined_filter = data_filter.and_filter([geom_filter, clear_percent_filter, date_range_filter])


    async with Session() as sess:
        cl = DataClient(sess)
        request = await cl.create_search(name='test_search', search_filter=combined_filter, item_types=item_type)
        items =  cl.run_search(search_id=request['id'])
        item_list = [i async for i in items]
        
        return item_list


async def create_and_download(client, order_detail, directory):
    """Make an order, wait for completion, download files as a single task."""

    timeout = httpx.Timeout(10.0, read=None)

    with reporting.StateBar(state='creating') as reporter:
        order = await client.create_order(order_detail)
        reporter.update(state='created', order_id=order['id'])
        await client.wait(order['id'], callback=reporter.update_state)

    await client.download_order(order['id'], directory, progress_bar=True)


async def main():
    async with Session() as sess:
        
        client = sess.client('orders')

        ht_aoi = gpd.read_file(HT_SHP)
        tt_aoi = gpd.read_file(TT_SHP)
        
        items = await asyncio.gather(*[
            search_request(ht_aoi),
            search_request(tt_aoi)
        ])

        requests = create_requests(ht_aoi, tt_aoi, items)

        await asyncio.gather(*[
            # Downloading the images at the two download directories
            # Haiti Site Request
            create_and_download(client, requests[0], DOWNLOAD_DIR_HT),
            # TrinidadTobago Site Request
            #create_and_download(client, requests[1], DOWNLOAD_DIR_TT)
        ])


if __name__ == '__main__':
    asyncio.run(main())
    

