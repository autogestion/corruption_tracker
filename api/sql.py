
moderation_filter = """
    position(claim_claim.moderation IN 
        (SELECT claim_moderator.show_claims 
        FROM claim_moderator WHERE claim_moderator.id = 1)) <> 0
    """