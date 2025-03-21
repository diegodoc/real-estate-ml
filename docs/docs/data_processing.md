# Data Processing

This document outlines the steps taken to process the real estate dataset.

## Data Acquisition
The real estate dataset is collected from various sources and stored in the `data/raw/` directory.

## Data Cleaning
The following cleaning steps are performed:
- Handling missing values in property features
- Converting categorical variables to numerical format
- Standardizing price formats and currencies
- Normalizing area measurements
- Cleaning and standardizing location data

## Feature Engineering
New features created include:
- Price per square meter/foot
- Property age (from year built)
- Location-based features (neighborhood scores, proximity to amenities)
- Text features from descriptions (keyword extraction, sentiment analysis)
- Image features (architectural style, condition assessment)
- Amenity counts and categories

## Dataset Features Description

### Property Classification Features

#### MSSubClass: Dwelling Type
| Code | Description |
|------|-------------|
| 20 | 1-STORY 1946 & NEWER ALL STYLES |
| 30 | 1-STORY 1945 & OLDER |
| 40 | 1-STORY W/FINISHED ATTIC ALL AGES |
| 45 | 1-1/2 STORY - UNFINISHED ALL AGES |
| 50 | 1-1/2 STORY FINISHED ALL AGES |
| 60 | 2-STORY 1946 & NEWER |
| 70 | 2-STORY 1945 & OLDER |
| 75 | 2-1/2 STORY ALL AGES |
| 80 | SPLIT OR MULTI-LEVEL |
| 85 | SPLIT FOYER |
| 90 | DUPLEX - ALL STYLES AND AGES |
| 120 | 1-STORY PUD (Planned Unit Development) - 1946 & NEWER |
| 150 | 1-1/2 STORY PUD - ALL AGES |
| 160 | 2-STORY PUD - 1946 & NEWER |
| 180 | PUD - MULTILEVEL - INCL SPLIT LEV/FOYER |
| 190 | 2 FAMILY CONVERSION - ALL STYLES AND AGES |

#### MSZoning: Zoning Classification
| Code | Description |
|------|-------------|
| A | Agriculture |
| C | Commercial |
| FV | Floating Village Residential |
| I | Industrial |
| RH | Residential High Density |
| RL | Residential Low Density |
| RP | Residential Low Density Park |
| RM | Residential Medium Density |

### Property Characteristics

#### LotFrontage
Linear feet of street connected to property

#### LotArea
Lot size in square feet

#### Street: Road Access
- `Grvl`: Gravel
- `Pave`: Paved

#### Alley: Alley Access
- `Grvl`: Gravel
- `Pave`: Paved
- `NA`: No alley access

#### LotShape: Property Shape
- `Reg`: Regular
- `IR1`: Slightly irregular
- `IR2`: Moderately Irregular
- `IR3`: Irregular

#### LandContour: Terrain Flatness
- `Lvl`: Near Flat/Level
- `Bnk`: Banked - Quick and significant rise from street grade to building
- `HLS`: Hillside - Significant slope from side to side
- `Low`: Depression

#### Utilities: Available Utilities
- `AllPub`: All public Utilities (E,G,W,& S)
- `NoSewr`: Electricity, Gas, and Water (Septic Tank)
- `NoSeWa`: Electricity and Gas Only
- `ELO`: Electricity only

#### LotConfig: Lot Configuration
- `Inside`: Inside lot
- `Corner`: Corner lot
- `CulDSac`: Cul-de-sac
- `FR2`: Frontage on 2 sides of property
- `FR3`: Frontage on 3 sides of property

#### LandSlope: Property Slope
- `Gtl`: Gentle slope
- `Mod`: Moderate Slope
- `Sev`: Severe Slope

### Neighborhood Information

#### Neighborhood: Physical Locations
| Code | Description |
|------|-------------|
| Blmngtn | Bloomington Heights |
| Blueste | Bluestem |
| BrDale | Briardale |
| BrkSide | Brookside |
| ClearCr | Clear Creek |
| CollgCr | College Creek |
| Crawfor | Crawford |
| Edwards | Edwards |
| Gilbert | Gilbert |
| IDOTRR | Iowa DOT and Rail Road |
| MeadowV | Meadow Village |
| Mitchel | Mitchell |
| Names | North Ames |
| NoRidge | Northridge |
| NPkVill | Northpark Villa |
| NridgHt | Northridge Heights |
| NWAmes | Northwest Ames |
| OldTown | Old Town |
| SWISU | South & West of Iowa State University |
| Sawyer | Sawyer |
| SawyerW | Sawyer West |
| Somerst | Somerset |
| StoneBr | Stone Brook |
| Timber | Timberland |
| Veenker | Veenker |

### Proximity Features

#### Condition1: Primary Proximity Condition
- `Artery`: Adjacent to arterial street
- `Feedr`: Adjacent to feeder street
- `Norm`: Normal
- `RRNn`: Within 200' of North-South Railroad
- `RRAn`: Adjacent to North-South Railroad
- `PosN`: Near positive off-site feature (park, greenbelt, etc.)
- `PosA`: Adjacent to positive off-site feature
- `RRNe`: Within 200' of East-West Railroad
- `RRAe`: Adjacent to East-West Railroad

#### Condition2: Secondary Proximity Condition
(Same codes as Condition1, if more than one is present)

### Building Information

#### BldgType: Building Type
- `1Fam`: Single-family Detached
- `2FmCon`: Two-family Conversion
- `Duplx`: Duplex
- `TwnhsE`: Townhouse End Unit
- `TwnhsI`: Townhouse Inside Unit

#### HouseStyle: House Style
- `1Story`: One story
- `1.5Fin`: One and one-half story: 2nd level finished
- `1.5Unf`: One and one-half story: 2nd level unfinished
- `2Story`: Two story
- `2.5Fin`: Two and one-half story: 2nd level finished
- `2.5Unf`: Two and one-half story: 2nd level unfinished
- `SFoyer`: Split Foyer
- `SLvl`: Split Level

### Quality and Condition Ratings

#### OverallQual: Overall Material and Finish Quality
| Rating | Description |
|--------|-------------|
| 10 | Very Excellent |
| 9 | Excellent |
| 8 | Very Good |
| 7 | Good |
| 6 | Above Average |
| 5 | Average |
| 4 | Below Average |
| 3 | Fair |
| 2 | Poor |
| 1 | Very Poor |

#### OverallCond: Overall Condition Rating
| Rating | Description |
|--------|-------------|
| 10 | Very Excellent |
| 9 | Excellent |
| 8 | Very Good |
| 7 | Good |
| 6 | Above Average |
| 5 | Average |
| 4 | Below Average |
| 3 | Fair |


