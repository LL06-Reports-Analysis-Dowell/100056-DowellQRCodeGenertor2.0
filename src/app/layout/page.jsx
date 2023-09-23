"use client";
import React, { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import DisplayQRCodes from "./DisplayQRCodes";
import { toast } from "react-toastify";
import { Loader2 } from "lucide-react"
import { Input } from "@/components/ui/input";
import { Loader } from "./Loader";

const QRCodeForm = ({userInfo}) => {
  // get api 
  const [qrcodes, setQRCodes] = useState();
  const [loading, setLoading] = useState(false)
   

  const fetchQrCodes = async () => {
    const apiUrl = `https://uxlivinglab100106.pythonanywhere.com/api/qrcode/v1/qr-code/?user_id=${userInfo?.userID}`;

    try {
      setLoading(true)
      const response = await fetch(apiUrl);

      const responseData = await response.json();
      console.log("status", responseData.ok);
      setQRCodes(responseData?.response?.data);
      setLoading(false)
    } catch (error) {
      setLoading(false)
      console.error(error.message);
    }
  };


  useEffect(() => {
    fetchQrCodes();
  }, []);

  // post api 
  let [displayData, setDisplayData] = useState({});
  const [submitting, setSubmitting] = useState(false);

  let [formData, setFormData] = useState({
    company_id: userInfo?.client_admin_id,
    user_id: userInfo?.userID,
    link: "",
    name: "",
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  const handleSubmit = async () => {
    
    if (formData.link != "") {
      const apiUrl =
      `https://uxlivinglab100106.pythonanywhere.com/api/qrcode/v1/qr-code/`
      const requestData = {
        company_id: formData.company_id,
        user_id: formData.user_id,
        link: formData.link,
        name: formData.name,
      };
      try {
        setSubmitting(true);
        const response = await fetch(apiUrl, {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify(requestData),
        });

        const responseData = await response.json();

        console.log("API response:", responseData);
        if(responseData.success){
          setSubmitting(false);
          toast.success(`Link Shortened Successfully`);
          formData.link=""
          fetchQrCodes()
        }
        if (responseData.link) {
          toast.info(`Enter a valid URL`);
          setSubmitting(False)
        } else if (responseData.name) {
          toast.info(`Name is required`);
          setSubmitting(False)
        } else {
          setSubmitting(False)
          await setDisplayData(responseData.qrcode);
          console.log("Put API response", await displayData);
        }
      } catch (error) {
        setSubmitting(false);
        console.error(error.message);
      }

    } else {
      setSubmitting(false)
    }
  };

  
  
  return (

        <>
          
          <div>
            <div className="mainCard pb-8 h-screen w-screen rounded-lg overflow-auto">
              <h1 className="text-2xl mt-5 text-center p-5 text-white font-bold">
                Welcome to Dowell URL Shortener <span className="name">{userInfo?.first_name}</span>
              </h1>
              <p className="subText text-center">
                Create short and memorable links in seconds
              </p>
              <div className="container mx-auto p-4 my-5">
                <div className="flex flex-col md:flex-row justify-center items-center space-y-2 md:space-y-0 md:space-x-2">
                  <div className="flex flex-col md:flex-row w-full md:w-1/2 space-y-2 md:space-y-0 md:space-x-2">
                    <Input
                      type="text"
                      name="link"
                      value={formData.link || ""}
                      onChange={handleChange}
                      placeholder="Enter the link here"
                      className="w-full md:w-3/4 px-4 py-2 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring focus:border-blue-500 justify-center items-center space-y-2"
                    />
                    <Input
                      type="text"
                      name="name"
                      value={formData.name || ""}
                      onChange={handleChange}
                      placeholder="Name"
                      className="w-full md:w-1/4 px-4 py-2 bg-white border border-gray-300 rounded-xl focus:outline-none focus:ring focus:border-blue-500"
                    />
                  </div>
                  
                  <button
                    disabled={submitting || formData.link === "" || formData.name === ""}
                    type="button"
                    onClick={handleSubmit}
                    className="w-full md:w-auto px-4 py-2 btnStyle text-white rounded-xl focus:outline-none focus:ring flex items-center justify-center"
                  >
                    {submitting ? <Loader2 className="text-4xl animate-spin" /> : 'Submit'}
                  </button>{" "}
                </div>
              </div>
              
              <div>
                {loading ? <Loader /> : qrcodes?.length > 0 ? <DisplayQRCodes qrcodes={qrcodes} getUserInfo={fetchQrCodes}/> : "No Links Found"}
              </div>
            </div>
          </div>
        </>
  );
};

export default QRCodeForm;
