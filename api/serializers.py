
from rest_framework import serializers
# from rest_framework.reverse import reverse
from claim.models import Claim


class ClaimSerializer(serializers.ModelSerializer):

    # links = serializers.SerializerMethodField()

    class Meta:
        model = Claim
        fields = ('text', 'created', 'live', 'organization',
                  'servant', 'complainer', 'claim_type',
                  # 'links'
                  )

    # def get_links(self, obj):
    #     request = self.context['request']
    #     return {
    #         'self': reverse('claim-detail',
    #          kwargs={'pk': obj.pk}, request=request),
    #     }
