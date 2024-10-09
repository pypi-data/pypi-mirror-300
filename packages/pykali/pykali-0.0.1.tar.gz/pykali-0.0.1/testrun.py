from pykali.modules.genome import Genome
from pykali.modules.genomeset import GenomeSet
from pykali.modules.bands import Bands


bands = GenomeSet(
        Genome.fetch("EU490707", "info@pharm.chula.ac.th"),
        Genome.fetch("NZ_HG937516", "info@pharm.chula.ac.th")
    ).electrophorese('AAAAA', 30)
    
print(bands.distance())