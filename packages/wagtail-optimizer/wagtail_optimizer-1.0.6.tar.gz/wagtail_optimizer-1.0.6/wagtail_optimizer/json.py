from django.core.serializers.json import (
    DjangoJSONEncoder,
)

class WagtailOptimizerJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if hasattr(o, 'to_json'):
            return o.to_json()
        return super().default(o)
    
class ExpandedWagtailOptimizerJSONEncoder(DjangoJSONEncoder):
    def default(self, o):
        if hasattr(o, 'to_json_expanded'):
            return o.to_json_expanded()
        return super().default(o)