import { useEffect } from 'react';

function initializeMap(latitude, longitude, mapElementId) {
  const map = new window.google.maps.Map(document.getElementById(mapElementId), {
    center: { lat: latitude, lng: longitude },
    zoom: 12,
  });
  new window.google.maps.Marker({
    position: { lat: latitude, lng: longitude },
    map: map,
  });
}

function CompanyList() {
  const [companies, setCompanies] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/companies')
      .then(response => {
        setCompanies(response.data);
        response.data.forEach(company => {
          initializeMap(company.latitude, company.longitude, `map-${company.id}`);
        });
      })
      .catch(error => console.error("There was an error fetching the companies!", error));
  }, []);

  return (
    <div>
      <h2>Companies</h2>
      <ul>
        {companies.map(company => (
          <li key={company.id}>
            {company.name} - {company.address}
            <br />
            Latitude: {company.latitude}, Longitude: {company.longitude}
            <br />
            <div id={`map-${company.id}`} style={{ height: '200px', width: '300px' }}></div>
            <br />
          </li>
        ))}
      </ul>
    </div>
  );
}
