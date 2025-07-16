"""
OpenSilex API Client - Mock Data Module
Generates mock data for testing and development
"""

from faker import Faker
from typing import List
from modules.projects import ProjectCreationData
from modules.experiments import ExperimentCreationData
from modules.scientific_objects import ScientificObjectCreationData
from modules.devices import DeviceCreationData
from modules.organizations import OrganizationCreationData
from modules.persons import PersonCreationData
from modules.sites import SiteCreationData
from modules.facilities import FacilityCreationData
from modules.variables import VariableCreationData

# Initialize Faker
fake = Faker()

class MockClient:
    """
    Client for generating mock data
    """
    
    def __init__(self):
        """
        Initialize Mock client
        """
        pass

    def create_mock_project(self) -> ProjectCreationData:
        """
        Generates a single mock project using the Faker library.
        
        Returns:
            A ProjectCreationData object with mock data.
        """
        start_date = fake.past_date(start_date="-5y")
        end_date = fake.future_date(end_date="+5y")
        
        return ProjectCreationData(
            name=fake.company() + " Project",
            shortname=fake.bs(),
            description=fake.text(max_nb_chars=200),
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            homepage=fake.url(),
            objective=fake.sentence(nb_words=10),
            keywords=[fake.word() for _ in range(5)],
            related_projects=[],
            coordinators=[],
            scientific_contacts=[],
            administrative_contacts=[]
        )

    def create_mock_projects(self, num_projects: int) -> List[ProjectCreationData]:
        """
        Generates a list of mock projects.
        
        Args:
            num_projects: The number of mock projects to generate.
            
        Returns:
            A list of ProjectCreationData objects.
        """
        return [self.create_mock_project() for _ in range(num_projects)]

    def create_mock_experiment(self, project_uri: str) -> ExperimentCreationData:
        """
        Generates a single mock experiment.
        
        Args:
            project_uri: The URI of the project this experiment belongs to.
            
        Returns:
            An ExperimentCreationData object with mock data.
        """
        start_date = fake.past_date(start_date="-2y")
        end_date = fake.future_date(end_date="+2y")

        return ExperimentCreationData(
            name=fake.catch_phrase(),
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d'),
            description=fake.text(max_nb_chars=150),
            objective=fake.sentence(nb_words=8),
            project=project_uri,
            is_public=fake.boolean(),
            contacts=[],
            technical_supervisors=[],
            scientific_supervisors=[],
            groups=[]
        )

    def create_mock_experiments(self, num_experiments: int, project_uri: str) -> List[ExperimentCreationData]:
        """
        Generates a list of mock experiments.
        
        Args:
            num_experiments: The number of mock experiments to generate.
            project_uri: The URI of the project these experiments belong to.
            
        Returns:
            A list of ExperimentCreationData objects.
        """
        return [self.create_mock_experiment(project_uri) for _ in range(num_experiments)]

    def create_mock_scientific_object(self, experiment_uri: str) -> ScientificObjectCreationData:
        """
        Generates a single mock scientific object.
        
        Args:
            experiment_uri: The URI of the experiment this object belongs to.
            
        Returns:
            A ScientificObjectCreationData object with mock data.
        """
        return ScientificObjectCreationData(
            name=fake.word(),
            rdf_type="http://www.opensilex.org/vocabulary/oeso#Plot",
            experiment=experiment_uri,
            relations=[]
        )

    def create_mock_scientific_objects(self, num_objects: int, experiment_uri: str) -> List[ScientificObjectCreationData]:
        """
        Generates a list of mock scientific objects.
        
        Args:
            num_objects: The number of mock objects to generate.
            experiment_uri: The URI of the experiment these objects belong to.
            
        Returns:
            A list of ScientificObjectCreationData objects.
        """
        return [self.create_mock_scientific_object(experiment_uri) for _ in range(num_objects)]

    def create_mock_device(self) -> DeviceCreationData:
        """
        Generates a single mock device.
        
        Returns:
            A DeviceCreationData object with mock data.
        """
        return DeviceCreationData(
            name=fake.word() + " Camera",
            rdf_type="http://www.opensilex.org/vocabulary/oeso#Camera",
            brand=fake.company(),
            model=fake.bothify(text='Model-##??'),
            serial_number=fake.ean(length=13),
            description=fake.text(max_nb_chars=100),
            relations=[]
        )

    def create_mock_devices(self, num_devices: int) -> List[DeviceCreationData]:
        """
        Generates a list of mock devices.
        
        Args:
            num_devices: The number of mock devices to generate.
            
        Returns:
            A list of DeviceCreationData objects.
        """
        return [self.create_mock_device() for _ in range(num_devices)]

    def create_mock_organization(self) -> OrganizationCreationData:
        """
        Generates a single mock organization.
        
        Returns:
            An OrganizationCreationData object with mock data.
        """
        return OrganizationCreationData(
            name=fake.company(),
            rdf_type="http://www.opensilex.org/vocabulary/oeso#Organization",
            address=fake.address(),
            phone=fake.phone_number(),
            email=fake.company_email(),
            website=fake.url(),
            description=fake.text(max_nb_chars=100),
            relations=[]
        )

    def create_mock_organizations(self, num_organizations: int) -> List[OrganizationCreationData]:
        """
        Generates a list of mock organizations.
        
        Args:
            num_organizations: The number of mock organizations to generate.
            
        Returns:
            A list of OrganizationCreationData objects.
        """
        return [self.create_mock_organization() for _ in range(num_organizations)]

    def create_mock_person(self) -> PersonCreationData:
        """
        Generates a single mock person.
        
        Returns:
            A PersonCreationData object with mock data.
        """
        return PersonCreationData(
            first_name=fake.first_name(),
            last_name=fake.last_name(),
            email=fake.email(),
            affiliation=fake.company(),
            phone_number=fake.phone_number()
        )

    def create_mock_persons(self, num_persons: int) -> List[PersonCreationData]:
        """
        Generates a list of mock persons.
        
        Args:
            num_persons: The number of mock persons to generate.
            
        Returns:
            A list of PersonCreationData objects.
        """
        return [self.create_mock_person() for _ in range(num_persons)]

    def create_mock_site(self, organization_uris: List[str] = None) -> SiteCreationData:
        """
        Generates a single mock site.
        
        Args:
            organization_uris: Optional list of organization URIs to attach the site to.
            
        Returns:
            A SiteCreationData object with mock data.
        """
        return SiteCreationData(
            name=fake.street_name(),
            address={
                "street": fake.street_address(),
                "city": fake.city(),
                "country": fake.country()
            },
            description=fake.text(max_nb_chars=100),
            geometry={
                "type": "Point",
                "coordinates": [float(fake.longitude()), float(fake.latitude())]
            },
            organizations=organization_uris if organization_uris else []
        )

    def create_mock_sites(self, num_sites: int, organization_uris: List[str] = None) -> List[SiteCreationData]:
        """
        Generates a list of mock sites.
        
        Args:
            num_sites: The number of mock sites to generate.
            organization_uris: Optional list of organization URIs to attach the sites to.
            
        Returns:
            A list of SiteCreationData objects.
        """
        return [self.create_mock_site(organization_uris) for _ in range(num_sites)]

    def create_mock_facility(self) -> FacilityCreationData:
        """
        Generates a single mock facility.
        
        Returns:
            A FacilityCreationData object with mock data.
        """
        return FacilityCreationData(
            name=fake.word() + " Greenhouse",
            facility_type="http://www.opensilex.org/vocabulary/oeso#Greenhouse",
            address={
                "street": fake.street_address(),
                "city": fake.city(),
                "zipCode": fake.postcode(),
                "country": fake.country()
            }
        )

    def create_mock_facilities(self, num_facilities: int) -> List[FacilityCreationData]:
        """
        Generates a list of mock facilities.
        
        Args:
            num_facilities: The number of mock facilities to generate.
            
        Returns:
            A list of FacilityCreationData objects.
        """
        return [self.create_mock_facility() for _ in range(num_facilities)]

    def create_mock_variable(self) -> VariableCreationData:
        """
        Generates a single mock variable.
        
        Returns:
            A VariableCreationData object with mock data.
        """
        return VariableCreationData(
            name=fake.word(),
            entity=fake.word(),
            characteristic=fake.word(),
            method=fake.word(),
            unit=fake.word(),
            trait=fake.word(),
            datatype="http://www.w3.org/2001/XMLSchema#string"
        )

    def create_mock_variables(self, num_variables: int) -> List[VariableCreationData]:
        """
        Generates a list of mock variables.
        
        Args:
            num_variables: The number of mock variables to generate.
            
        Returns:
            A list of VariableCreationData objects.
        """
        return [self.create_mock_variable() for _ in range(num_variables)]
