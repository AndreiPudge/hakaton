import React from 'react';
import logo from '../assets/logo.jpg'



const Header = () =>{
    return (
      <header>
      <div className="container-fluid">
        <div className="container">
          <div className="header_navigation">
            <div className='left_side_header'>
               <div className='logo_div'><img src={logo} className="header_logo"/></div>
            </div>
           
          <div className="header_info">
            <h2 className="title_page">AI-серивис прогноза дохода клиентов</h2>
           </div>
           </div>
           </div>
           </div>
         </header>
       
  )
}

export default Header