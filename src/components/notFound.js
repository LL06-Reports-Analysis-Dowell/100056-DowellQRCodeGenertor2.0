// components/NotFound.js
import React from 'react';
import { QrCode } from 'lucide-react';

const NotFound = () => {
  return (
    <div className="flex flex-col justify-center mt-4 items-center">
      <QrCode size={64} className="disabledColor" />
      <h1 className="text-xl mt-4 disabledColor">No Links Found</h1>
    </div>
  );
};

export default NotFound;
