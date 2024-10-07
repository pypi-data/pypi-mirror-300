import argparse
from rest_framework import serializers
from py_populate_dcim.api.models import RefreshRequest
from py_populate_dcim_lib import api_main


class RefreshRequestSerializer(serializers.Serializer):
    debug = serializers.BooleanField(required=False)
    refresh_synergy_frames = serializers.BooleanField(required=False)
    create_oneview_server_devices = serializers.BooleanField(required=False)
    create_oneview_server_modules = serializers.BooleanField(required=False)
    create_oneview_server_interfaces = serializers.BooleanField(required=False)
    import_nautobot_types = serializers.BooleanField(required=False)

    def create(self, validated_data):
        """
        Create and return a new `RefreshRequest` instance, given the validated data.
        """
        api_args = argparse.Namespace()
        args_as_dict = vars(api_args)
        for arg in validated_data:
            args_as_dict[arg] = validated_data[arg]

        api_main(api_args)
        return RefreshRequest.objects.create(**validated_data)

    class Meta:
        model = RefreshRequest
        fields = ('id', 'debug', 'refresh_synergy_frames', 'create_oneview_server_devices', 'create_oneview_server_modules',
                  'create_oneview_server_interfaces', 'import_nautobot_types')
