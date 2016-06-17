from django.db import connection


moderation_filter = """
    position(claim_claim.moderation IN 
        (SELECT claim_moderator.show_claims 
        FROM claim_moderator WHERE claim_moderator.id = 1)) <> 0
    """

claim_to_polygon_join = """    
    LEFT OUTER JOIN geoinfo_polygon_organizations  ON (houses.polygon_id = geoinfo_polygon_organizations.polygon_id) 
    LEFT OUTER JOIN claim_organization ON (geoinfo_polygon_organizations.organization_id = claim_organization.id) 
    LEFT OUTER JOIN claim_claim ON (claim_organization.id = claim_claim.organization_id)  
"""


def get_claims_for_poly(polygon_id):
        cursor = connection.cursor()
        cursor.execute("""
            SELECT COUNT(*) AS "__count" FROM "claim_organization" 
                INNER JOIN "geoinfo_polygon_organizations" ON ("claim_organization"."id" = "geoinfo_polygon_organizations"."organization_id") 
                INNER JOIN "claim_claim" ON ("claim_organization"."id" = "claim_claim"."organization_id") 
                WHERE ("geoinfo_polygon_organizations"."polygon_id" = '%s' AND %s)                        
            """ % (polygon_id, moderation_filter))

        return cursor.fetchone()[0]


def get_sum_for_layers(layers_ids, level):
    cursor = connection.cursor()
    if level==4:
        cursor.execute("""
            SELECT claim_organization.id, COUNT(claim_claim.id) AS claims FROM claim_organization 
                LEFT OUTER JOIN claim_claim ON (claim_organization.id = claim_claim.organization_id) 
                WHERE (claim_organization.id IN (%s) AND %s )
                GROUP BY claim_organization.id                 
            """ % (','.join([str(x) for x in layers_ids]), moderation_filter)
            )

    elif level==3:
        cursor.execute("""
            SELECT district_id, SUM(claimz) as sum_claims FROM 
                (SELECT houses.layer_id as district_id, COUNT(claim_claim.id) AS claimz FROM geoinfo_polygon houses                    
                    %s
                    WHERE (houses.layer_id IN (%s) AND %s)
                    GROUP BY houses.polygon_id ) x
                GROUP BY district_id
        """ % (claim_to_polygon_join, ','.join(["'" + str(x) + "'" for x in layers_ids]), moderation_filter)
        )

    elif level==2:
        cursor.execute("""
            SELECT area_id, SUM(claimz) as sum_claims FROM 
                (SELECT districts.layer_id as area_id, COUNT(claim_claim.id) AS claimz FROM geoinfo_polygon districts
                    LEFT OUTER JOIN geoinfo_polygon houses  ON (houses.layer_id = districts.polygon_id)                    
                    %s
                    WHERE (districts.layer_id IN (%s) AND %s)
                    GROUP BY districts.polygon_id ) x
                GROUP BY area_id
        """ % (claim_to_polygon_join, ','.join(["'" + str(x) + "'" for x in layers_ids]), moderation_filter)
        )

    elif level==1:
        cursor.execute("""
            SELECT region_id, SUM(claimz) as sum_claims FROM 
                (SELECT areas.layer_id as region_id, COUNT(claim_claim.id) AS claimz FROM geoinfo_polygon areas                
                    LEFT OUTER JOIN geoinfo_polygon districts ON (districts.layer_id = areas.polygon_id)   
                    LEFT OUTER JOIN geoinfo_polygon houses ON (houses.layer_id = districts.polygon_id)                     
                    %s
                    WHERE (areas.layer_id IN (%s) AND %s)
                    GROUP BY areas.polygon_id ) x
                GROUP BY region_id
        """ % (claim_to_polygon_join, ','.join(["'" + str(x) + "'" for x in layers_ids]), moderation_filter)
        )

    elif level==0:
        cursor.execute("""
            SELECT root_id, SUM(claimz) as sum_claims FROM 
                (SELECT regions.layer_id as root_id, COUNT(claim_claim.id) AS claimz FROM geoinfo_polygon regions
                    LEFT OUTER JOIN geoinfo_polygon areas ON (areas.layer_id = regions.polygon_id)                
                    LEFT OUTER JOIN geoinfo_polygon districts ON (districts.layer_id = areas.polygon_id)   
                    LEFT OUTER JOIN geoinfo_polygon houses ON (houses.layer_id = districts.polygon_id)                     
                    %s
                    WHERE (regions.layer_id IN (%s) AND %s)
                    GROUP BY regions.polygon_id ) x
                GROUP BY root_id
        """ % (claim_to_polygon_join, ','.join(["'" + str(x) + "'" for x in layers_ids]), moderation_filter)
        )


    return dict(cursor.fetchall())


def get_max_for_layers(layer_id, level):
    layers_dict = {}
    cursor = connection.cursor()

    if level==4:
        # x = Polygon.objects.filter(layer_id=layer_id).annotate(claimz=Count('organizations__claim')) 
        
        cursor.execute("""
            SELECT layer_id, MAX(claimz) FROM 
                (SELECT houses.layer_id as layer_id, COUNT(claim_claim.id) AS claimz FROM geoinfo_polygon houses 
                        %s
                        WHERE (houses.layer_id IN (%s) AND %s)
                        GROUP BY houses.polygon_id ) x
                GROUP BY layer_id
        """ %   (claim_to_polygon_join, ','.join(["'" + str(x) + "'" for x in layer_id]), moderation_filter)
        )

    elif level==3:
        cursor = connection.cursor()
        cursor.execute("""
                SELECT district_id, MAX(claimz) as sum_claims FROM (
                    SELECT districts.layer_id as district_id, COUNT(claim_claim.id) AS claimz FROM geoinfo_polygon districts
                            LEFT OUTER JOIN geoinfo_polygon houses  ON (houses.layer_id = districts.polygon_id) 
                            %s
                            WHERE (districts.layer_id IN (%s) AND %s)
                            GROUP BY districts.polygon_id) x
                    GROUP BY district_id
        """ % (claim_to_polygon_join, ','.join(["'" + str(x) + "'" for x in layer_id]), moderation_filter)
        )       

    elif level==2:
        cursor.execute("""
                SELECT district_id, MAX(claimz) as sum_claims FROM (
                    SELECT areas.layer_id as district_id, COUNT(claim_claim.id) AS claimz FROM geoinfo_polygon areas
                            LEFT OUTER JOIN geoinfo_polygon districts  ON (districts.layer_id = areas.polygon_id)
                            LEFT OUTER JOIN geoinfo_polygon houses  ON (houses.layer_id = districts.polygon_id) 
                            %s
                            WHERE (areas.layer_id IN (%s) AND %s)
                            GROUP BY areas.polygon_id) x
                    GROUP BY district_id
        """ % (claim_to_polygon_join, ','.join(["'" + str(x) + "'" for x in layer_id]), moderation_filter)
        )

    elif level==1:
        cursor.execute("""
                SELECT district_id, MAX(claimz) as sum_claims FROM (
                    SELECT regions.layer_id as district_id, COUNT(claim_claim.id) AS claimz FROM geoinfo_polygon regions
                            LEFT OUTER JOIN geoinfo_polygon areas  ON (areas.layer_id = regions.polygon_id)
                            LEFT OUTER JOIN geoinfo_polygon districts  ON (districts.layer_id = areas.polygon_id)
                            LEFT OUTER JOIN geoinfo_polygon houses  ON (houses.layer_id = districts.polygon_id)
                            %s
                            WHERE (regions.layer_id IN (%s) AND %s)
                            GROUP BY regions.polygon_id) x
                    GROUP BY district_id
        """ % (claim_to_polygon_join, ','.join(["'" + str(x) + "'" for x in layer_id]), moderation_filter)
        )

    return dict(cursor.fetchall())

    
    # layers_tuples = cursor.fetchall()
    # max_claims_value = dict(layers_tuples)

    # else:
    #     cached = cache.get('max_claims_for::%s' % layer_id)
    #     # cached = None
    #     if cached is not None:
    #         max_claims_value = cached
    #     else:
    #         brothers = Polygon.objects.filter(layer_id=layer_id)
    #         max_claims_value = max([x.total_claims for x in brothers])

    #         cache.set('max_claims_for::%s' % layer_id, max_claims_value, 300)

    # return max_claims_value