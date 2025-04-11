import React from 'react';
import AllCVs from './ALLCVs';
import CVUpload from './CVUpload'


const HRPageThree = () => {
  return (
    <div >
      <h2 >HR Page 2: Create & View Job Descriptions</h2>
      <CVUpload />
      <hr />
      <AllCVs />
    </div>
  );
};

export default HRPageThree;
