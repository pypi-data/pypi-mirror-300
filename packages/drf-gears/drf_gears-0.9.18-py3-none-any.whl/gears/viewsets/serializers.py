class SerializersMixin(object):
    """
    SerializersMixin implements the mapping logic for managing serializers according
    to the action, request, type so on.

    Example:
        serializers = dict(
            None=DefaultSerializer,  # will be used this one if none of rest are not suitable
            list=ListSerializer,  # will be used for the list() method of ViewSet
            retrieve=RetrieveSerializer,  # will be used for the retrieve() method of ViewSet
            create=CreateSerializer,  # will be used for the create() method of ViewSet
            update=UpdateSerializer,  # will be used for the update() method of ViewSet
            partial_update=UpdateSerializer,  # will be used for the partial_update() method of ViewSet
            destroy=DestroySerializer,  # will be used for the destroy() method of ViewSet
            custom_action=CustomActionSerializer,  # will be used for the custom ViewSet method named as `custom_action`
            my_serializer=MySerializer,  # will be used if the serializer_name attribute is set

            # NOT IMPLEMENTED YET
            # get=GetOnlySerializer,  # will be used for the GET requests of ViewSet
            # post=PostOnlySerializer,  # will be used for the POST requests of ViewSet
            # put=PutOnlySerializer,  # will be used for the PUT requests of ViewSet
            # patch=PatchOnlySerializer,  # will be used for the PATCH requests of ViewSet
            # delete=DeleteOnlySerializer,  # will be used for the DELETE requests of ViewSet

        )

    Priority: specified by name, action, method, default
    """
    serializers = {}
    serializer_class = None
    default_serializer_name = None  # None as a key for dict
    _serializers = {
        default_name: serializer_class,
    }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.serializer_class and not self.serializers.get(self.default_name):
            raise ValueError(
                "Need to specify either 'serializer_class' or "
                "'serializers default' class"
            )
        self._serializers.update(self.serializers)

    def get_serializer_class(self, serializer_name=None):
        return self.serializers.get(serializer_name) \
               or self.serializers.get(self.action) \
               or self.serializers.get(self.default_serializer_name) \
               or super().get_serializer_class()

    # TODO: This is a good refactoring but it must be additionally tested
    # def get_serializer_class(self, serializer_name=None):
    #     return (
    #         self.__by_name(serializer_name)
    #         or self.__by_action()
    #         or self.__default()
    #         or super().get_serializer_class()
    #     )

    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class(
            serializer_name=kwargs.pop('serializer_name', None)
        )
        kwargs['context'] = self.get_serializer_context()
        return serializer_class(*args, **kwargs)

    def __by_name(self, name: str):
        return self.serializers.get(name)

    def __by_action(self):
        return self.serializers.get(self.action)

    # def __by_method(self):
    #     return

    def __default(self):
        return self.serializers.get(self.default_serializer_name)
