import sys

from TCKUtils.utils import getProperties


def describe(tck, name, props, indentation):
    """Recurse down into this algorithm's properties, printing information on
    its inputs."""
    indent = indentation*' '

    def iprint(s):
        print('{}{}'.format(indent, s))

    if 'Particle' in props:
        # Have a Particle maker, no need to descend further
        iprint(props['Output'])
        return

    header_name = '\n{0}{1}\n{0}{2}'.format(indent, name, len(name)*'=')
    print(header_name)

    header_sel = '\n{0}Selection\n{0}---------'.format(indent)
    print(header_sel)

    if 'Code' in props:
        # We have a FilterDesktop
        iprint('Code: {}'.format(props['Code']))
    elif 'DaughtersCuts' in props:
        # We have a CombineParticles
        preambulo = eval(props['Preambulo'])
        iprint('DecayDescriptors: {}'.format(props['DecayDescriptors']))
        if preambulo:
            iprint('Preambulo:        {}'.format(preambulo))
        iprint('DaughtersCuts:    {}'.format(props['DaughtersCuts']))
        iprint('CombinationCut:   {}'.format(props['CombinationCut']))
        iprint('MotherCut:        {}'.format(props['MotherCut']))
    elif 'TisTosSpecs' in props:
        # We have a TisTosTagger
        iprint('TisTosSpecs:  {}'.format(props['TisTosSpecs']))
    else:
        assert False, 'Do not know the type of {}'.format(props)

    header_inputs = '\n{0}Inputs\n{0}------'.format(indent)
    print(header_inputs)

    inputs = eval(props['Inputs'])
    for input_name in inputs:
        assert input_name.startswith('Hlt2/')
        input_name = '.*/{}$'.format(input_name[len('Hlt2/'):])
        input_props = getProperties(tck, input_name)
        assert len(input_props) == 1
        input_name, input_props = getProperties(tck, input_name).items()[0]
        describe(tck, input_name, input_props, indentation + 4)


def selections(tck, line):
    assert line.startswith('Hlt2') and line.endswith('Turbo')
    decision_name = '.*{}Decision$'.format(line)
    decision_props = getProperties(tck, decision_name).values()[0]
    decision_inputs = eval(decision_props['InputSelection'])
    assert decision_inputs.startswith('TES:/Event/Hlt2/') and decision_inputs.endswith('/Particles')
    
    filter_name = '.*/{}$'.format(decision_inputs[len('TES:/Event/Hlt2/'):len(decision_inputs)-len('/Particles')])
    filter_props = getProperties(tck, filter_name)
    assert len(filter_props) == 1
    filter_name, filter_props = filter_props.items()[0]
    describe(tck, filter_name, filter_props, indentation=0)



def main():

    year = 2018
    
    #2016
    if year == 2016 :
        tck = 0x2137160e
    #2017
    elif year == 2017 :
        tck = 0x215517a7
    #2018
    elif year == 2018 :
        tck = 0x217a1801
    lines = [
        'Hlt2CharmHadLcpToPpKmPipTurbo',
        'Hlt2CharmHadInclLcpToKmPpPipBDTTurbo',
        'Hlt2CharmHadXiccpp2LcpKmPipPip_Lcp2PpKmPipTurbo'
    ]
    for line in lines:
        with open('{}.{}.selections.txt'.format(line,year), 'w') as f:
            sys.stdout = f
            selections(tck, line)

if __name__ == '__main__':
    main()
