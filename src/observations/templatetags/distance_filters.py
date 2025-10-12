from django import template
from decimal import Decimal

register = template.Library()


@register.filter
def humanize_large_number(value):
    """
    Convert a large number into a human-readable format.

    Examples:
    147191891269293 -> "147 trillion"
    5280000000000 -> "5.3 trillion"
    1500000000 -> "1.5 billion"
    """
    if not value:
        return value

    try:
        # Convert to float for easier calculation
        num = float(value)

        if num >= 1e15:  # Quadrillion
            return f"{num/1e15:.1f} quadrillion"
        elif num >= 1e12:  # Trillion
            result = num / 1e12
            if result >= 100:
                return f"{result:.0f} trillion"
            else:
                return f"{result:.1f} trillion"
        elif num >= 1e9:  # Billion
            result = num / 1e9
            if result >= 100:
                return f"{result:.0f} billion"
            else:
                return f"{result:.1f} billion"
        elif num >= 1e6:  # Million
            result = num / 1e6
            if result >= 100:
                return f"{result:.0f} million"
            else:
                return f"{result:.1f} million"
        elif num >= 1e3:  # Thousand
            result = num / 1e3
            if result >= 100:
                return f"{result:.0f} thousand"
            else:
                return f"{result:.1f} thousand"
        else:
            return f"{num:.0f}"

    except (ValueError, TypeError, OverflowError):
        return value


@register.filter
def humanize_distance_miles(value):
    """
    Specifically format astronomical distances in miles with context.

    Examples:
    147191891269293 -> "147 trillion miles"
    """
    if not value:
        return "distance unknown"

    humanized = humanize_large_number(value)
    if humanized != value:  # If it was successfully humanized
        return f"{humanized} miles"
    else:
        return f"{value} miles"


@register.filter
def get_apparent_magnitude(api_payload):
    """
    Extract apparent magnitude (V-band) from SIMBAD API payload.

    Returns the V-band magnitude as a formatted string, or None if not available.
    """
    if not api_payload:
        return None

    try:
        v_magnitude = api_payload.get("V")
        if v_magnitude and v_magnitude != "--":
            # Convert to float and format to 2 decimal places
            mag_float = float(v_magnitude)
            return f"{mag_float:.2f}"
    except (ValueError, TypeError):
        pass

    return None


@register.filter
def get_object_type(api_payload):
    """
    Extract and humanize object type from SIMBAD API payload.

    Converts SIMBAD object type codes to human-readable descriptions.
    """
    if not api_payload:
        return None

    otype = api_payload.get("otype")
    if not otype:
        return None

    # Dictionary mapping SIMBAD object types to human-readable descriptions
    # Based on SIMBAD's official object type hierarchy: http://simbad.u-strasbg.fr/simbad/sim-display?data=otypes
    object_type_mapping = {
        # Stars and stellar objects
        "*": "Star",
        "**": "Double or Multiple Star",
        "PM*": "High Proper Motion Star",
        "HV*": "High Velocity Star",
        "V*": "Variable Star",
        "Ir*": "Irregular Variable Star",
        "Or*": "Variable Star in Orion Nebula",
        "RI*": "Variable Star with Rapid Variations",
        "Er*": "Eruptive Variable Star",
        "Fl*": "Flare Star",
        "FU*": "FU Orionis Star",
        "RC*": "Variable Star of R CrB Type",
        "RC?": "Variable Star of R CrB Type (Candidate)",
        "Ro*": "Rotationally Variable Star",
        "a2*": "Variable Star of Alpha2 CVn Type",
        "Psr": "Pulsar",
        "BY*": "Variable Star of BY Dra Type",
        "RS*": "Variable Star of RS CVn Type",
        "Pu*": "Pulsating Variable Star",
        "RR*": "Variable Star of RR Lyr Type",
        "Ce*": "Cepheid Variable Star",
        "dS*": "Delta Scuti Variable Star",
        "RV*": "Variable Star of RV Tau Type",
        "WV*": "Variable Star of W Vir Type",
        "bC*": "Variable Star of Beta Cep Type",
        "cC*": "Classical Cepheid Variable Star",
        "gD*": "Gamma Doradus Variable Star",
        "SX*": "Variable Star of SX Phe Type",
        "LP*": "Long Period Variable Star",
        "Mi*": "Variable Star of Mira Cet Type",
        "sr*": "Semi-Regular Variable Star",
        "S*": "S Star",
        "s*r": "Semi-Regular Variable Star",
        "s*b": "Semi-Regular Variable Star (subtype B)",
        "AB*": "Asymptotic Giant Branch Star",
        "C*": "Carbon Star",
        "N*": "Wolf-Rayet Star",
        "WD*": "White Dwarf",
        "ZZ*": "Variable White Dwarf of ZZ Cet Type",
        "BD*": "Brown Dwarf",
        "LM*": "Low Mass Star",
        "YS*": "Young Stellar Object",
        "pA*": "Post-AGB Star",
        "WU*": "W UMa-type Eclipsing Binary",
        "Ae*": "Herbig Ae/Be Star",
        "Em*": "Emission Line Star",
        "Be*": "Be Star",
        "BS*": "Blue Straggler Star",
        "RG*": "Red Giant Branch Star",
        "sg*": "Evolved Supergiant Star",
        "s*y": "Symbiotic Star",
        "HS*": "Hot Subdwarf",
        "WR*": "Wolf-Rayet Star",
        "of*": "Of Star",
        "NO*": "Nova",
        "NL*": "Nova-like Star",
        "DN*": "Dwarf Nova",
        "XB*": "X-ray Binary",
        "LXB": "Low Mass X-ray Binary",
        "HXB": "High Mass X-ray Binary",
        # Stellar associations and clusters
        "As*": "Association of Stars",
        "St*": "Stellar Stream",
        "MGr": "Moving Group",
        "EB*": "Eclipsing Binary",
        "Al*": "Algol-type Eclipsing Binary",
        "bL*": "Beta Lyrae-type Eclipsing Binary",
        "CV*": "Cataclysmic Variable Star",
        "Pec*": "Peculiar Star",
        # Star clusters
        "Cl*": "Star Cluster",
        "GlC": "Globular Cluster",
        "OpC": "Open Cluster",
        # Nebulae
        "Neb": "Nebula",
        "PN": "Planetary Nebula",
        "SNR": "Supernova Remnant",
        "RNe": "Reflection Nebula",
        "ENe": "Emission Nebula",
        "DNe": "Dark Nebula",
        "HII": "HII Region",
        "MoC": "Molecular Cloud",
        "glb": "Globule",
        "cor": "Dense Core",
        "SFR": "Star Forming Region",
        "BiC": "Bright Cloud",
        # Galaxies
        "G": "Galaxy",
        "GiC": "Galaxy in Cluster",
        "GiG": "Galaxy in Group",
        "GPa": "Galaxy Pair",
        "GTr": "Galaxy Triple",
        "CGG": "Compact Group of Galaxies",
        "PaG": "Pair of Galaxies",
        "SpG": "Spiral Galaxy",
        "S0G": "Lenticular Galaxy",
        "EG": "Elliptical Galaxy",
        "IG": "Irregular Galaxy",
        "SBG": "Barred Spiral Galaxy",
        "BCG": "Blue Compact Galaxy",
        "LSB": "Low Surface Brightness Galaxy",
        "H2G": "HII Galaxy",
        "EmG": "Emission-line Galaxy",
        "SyG": "Seyfert Galaxy",
        "Sy1": "Seyfert 1 Galaxy",
        "Sy2": "Seyfert 2 Galaxy",
        "rG": "Radio Galaxy",
        "AG*": "Active Galaxy Nucleus",
        "QSO": "Quasar",
        "Bz*": "Blazar",
        "BLL": "BL Lac Object",
        "OVV": "Optically Violently Variable Object",
        "Lys": "LINER-type Active Galaxy Nucleus",
        # Solar system objects
        "Sun": "Sun",
        "Pla": "Planet",
        "DPl": "Dwarf Planet",
        "Moo": "Moon",
        "sat": "Satellite",
        "Ast": "Asteroid",
        "Com": "Comet",
        "MeT": "Meteor",
        # Other objects
        "err": "Not an Object (Error, Artefact, ...)",
        "?": "Object of Unknown Nature",
        "mul": "Composite Object",
        "reg": "Region Defined in the Sky",
        "vid": "Underdense Region of the Universe",
        "SCG": "Supercluster of Galaxies",
        "ClG": "Cluster of Galaxies",
        "GrG": "Group of Galaxies",
        "CGb": "Compact Group Member",
        "LeI": "Gravitationally Lensed Image",
        "LeG": "Gravitationally Lensed Image of a Galaxy",
        "LeQ": "Gravitationally Lensed Image of a Quasar",
        "LyA": "Lyman Alpha Emitter",
        "SN*": "SuperNova",
        "SNI": "Type I Supernova",
        "SNII": "Type II Supernova",
        "gLe": "Gravitational Lens",
        "gLS": "Gravitational Lens System",
        "GWE": "Gravitational Wave Event",
        "..?": "Possible Gravitational Wave Event",
        "TDE": "Tidal Disruption Event",
        "ISM": "Interstellar Medium",
        "PoC": "Part of Cloud",
        "PoG": "Part of Galaxy",
        "Rad": "Radio Source",
        "mR": "Metric Radio Source",
        "cm": "Centimetric Radio Source",
        "mm": "Millimetric Radio Source",
        "smm": "Sub-Millimetric Source",
        "HI": "HI (21cm) Source",
        "rB": "Radio Burst",
        "Mas": "Maser",
        "IR": "Infra-Red Source",
        "FIR": "Far-Infrared Source",
        "NIR": "Near-Infrared Source",
        "MIR": "Mid-Infrared Source",
        "THz": "TeraHertz Source",
        "blu": "Blue Object",
        "UV": "UV-emission Source",
        "X": "X-ray Source",
        "ULX": "Ultra-Luminous X-ray Source",
        "gam": "Gamma-ray Source",
        "gB": "Gamma-ray Burst",
        "grv": "Gravitational Source",
        "Lev": "(Micro)Lensing Event",
        "IntG": "Interacting Galaxies",
        "BH": "Black Hole",
    }

    return object_type_mapping.get(otype, f"Unknown ({otype})")


@register.filter
def get_spectral_type(api_payload):
    """
    Extract spectral type from SIMBAD API payload.
    """
    if not api_payload:
        return None

    sp_type = api_payload.get("sp_type")
    if sp_type and sp_type != "--":
        return sp_type

    return None


# decorator allows registering of custom filters to be used with '|' syntax, in django templates
@register.filter
def extract_date_from_slug(slug):
    """
    Extract the date part from a session slug.

    Examples:
    "1-2025-10-11-1" -> "2025-10-11"
    "2-2024-12-25-3" -> "2024-12-25"
    """
    # Split by hyphen and take the middle part (assuming format: number-YYYY-MM-DD-number)
    parts = slug.split("-")
    if len(parts) >= 4:
        # Extract the date parts (YYYY-MM-DD)
        return f"{parts[1]}-{parts[2]}-{parts[3]}"

    return slug
