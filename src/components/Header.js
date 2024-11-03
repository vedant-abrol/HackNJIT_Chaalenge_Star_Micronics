import React from 'react';
import starLogo from '/Users/vedantabrol/dynamic-pricing-dashboard/src/star_logo.png'; 

function Header() {
  return (
    <header className="App-header">
      <img src={starLogo} alt="Star Micronics Logo" className="App-logo" />
      <h1>Dynamic Pricing Dashboard</h1>
    </header>
  );
}

export default Header;
