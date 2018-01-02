from astropy.modeling.core import Model


class Mapping(Model):
    def __init__(self, mapping):
        self._inputs = tuple('x' + str(idx)
                             for idx in range(max(mapping) + 1))
        self._outputs = tuple('x' + str(idx) for idx in range(len(mapping)))
        self._mapping = mapping
        super(NewAxes, self).__init__()

    def __call__(self, *args):
        return self.evaluate(*args)

    @property
    def name(self):
        return 'Mapping({0})'.format(self.mapping)

    @property
    def inputs(self):
        return self._inputs

    @property
    def outputs(self):
        return self._outputs

    @property
    def mapping(self):
        return self._mapping

    def evaluate(self, *args):
        if len(args) < self.n_inputs:
            raise TypeError('{0} expects at most {1} inputs; got {2}'.format(
                self.name, self.n_inputs, len(args)))

        result = tuple(args[idx] for idx in self._mapping)

        if self.n_outputs == 1:
            return result[0]

        return result

    @property
    def inverse(self):
        try:
            mapping = tuple(self.mapping.index(idx)
                            for idx in range(self.n_inputs))
        except ValueError:
            raise NotImplementedError(
                "Mappings such as {0} that drop one or more of their inputs "
                "are not invertible at this time.".format(self.mapping))

        return self.__class__(mapping)


class NewAxes(Model):
    def __init__(self, mapping):
        #self._inputs = tuple('x' + str(idx)
                             #for idx in range(max(mapping) + 1))
        #self._outputs = tuple('x' + str(idx) for idx in range(len(mapping)))
        self._mapping = mapping
        super(Mapping, self).__init__()

    def __call__(self, *args):
        return self.evaluate(*args)

    @property
    def name(self):
        return 'NewAxes(output: {0})'.format(self.mapping)

    #@property
    #def inputs(self):
        #return self._inputs

    #@property
    #def outputs(self):
        #return self._outputs

    @property
    def mapping(self):
        return self._mapping

    def evaluate(self, *args):
        #if len(args) < self.n_inputs:
            #raise TypeError('{0} expects at most {1} inputs; got {2}'.format(
                #self.name, self.n_inputs, len(args)))

        result = tuple(args[idx] for idx in self._mapping)

        if self.n_outputs == 1:
            return result[0]

        return result

    @property
    def inverse(self):
        try:
            mapping = tuple(self.mapping.index(idx)
                            for idx in range(self.n_inputs))
        except ValueError:
            raise NotImplementedError(
                "Mappings such as {0} that drop one or more of their inputs "
                "are not invertible at this time.".format(self.mapping))

        return self.__class__(mapping)


class Identity(Mapping):
    def __init__(self, n_inputs):
        mapping = tuple(range(n_inputs))
        super(Identity, self).__init__(mapping)

    @property
    def name(self):
        return 'Identity({0})'.format(self.n_inputs)

    @property
    def inverse(self):
        return self