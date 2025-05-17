from pytest import PytestCollectionWarning

import warnings

warnings.filterwarnings("ignore", category=DeprecationWarning, module="pkg_resources")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="pygame.pkgdata")
warnings.filterwarnings("ignore", category=PytestCollectionWarning)