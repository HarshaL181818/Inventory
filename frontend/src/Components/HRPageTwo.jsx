import React from 'react';
import JobDescriptionInput from './JobDescriptionInput';
import AllJobDescriptions from './AllJobDescriptions';

const HRPageTwo = () => {
  return (
    <div>
      <h2 >HR Page 2: Create & View Job Descriptions</h2>
      <JobDescriptionInput />
      <hr className="my-4" />
      <AllJobDescriptions />
    </div>
  );
};

export default HRPageTwo;
