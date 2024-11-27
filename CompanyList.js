import React, { useState, useEffect } from 'react';
import axios from 'axios';

function CompanyList() {
  const [companies, setCompanies] = useState([]);

  useEffect(() => {
    axios.get('http://localhost:5000/companies')
      .then(response => setCompanies(response.data))
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

export default CompanyList;
