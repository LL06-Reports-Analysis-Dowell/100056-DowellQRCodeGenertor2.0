/* eslint-disable react-hooks/exhaustive-deps */
/* eslint-disable @next/next/no-img-element */
"use client";
import React, { useState, useEffect } from "react";
import { useSearchParams } from "next/navigation";
import DisplayQRCodes from "./DisplayQRCodes";
import { toast } from "react-toastify";
import { Loader2, Search, X } from "lucide-react"
import { Input } from "@/components/ui/input";
import { Loader } from "./Loader";
import NotFound from "../../components/notFound"
import Link from "next/link";
import OccurenceModal from "../../components/Modal";
import axios from 'axios';

const QRCodeForm = (props) => {
  // get api 
  const [qrcodes, setQRCodes] = useState();
  const [loading, setLoading] = useState(false)

  const [occurrence, setOccurrence] = useState(null);
  const [showOccurrence, setShowOccurrence] = useState(false);
  const [loadingGetOccurence, setLoadingOccurence] = useState(false);
  const [modalOpen, setModalOpen] = useState(false);
   

  const fetchQrCodes = async () => {
    const apiUrl = `https://www.uxlive.me/api/qrcode/v1/qr-code/?user_id=${props.userInfo?.userID}`;

    try {
      setLoading(true)
      const response = await fetch(apiUrl);

      const responseData = await response.json();
      setQRCodes(responseData?.response);
      setLoading(false)
    } catch (error) {
      setLoading(false)
      console.error(error.message);
    }
  };

  const [ apiKey, setApiKey ] = useState()

  const fetchApiKey = async () => {
    const apiUrl = `https://100105.pythonanywhere.com/api/v3/user/?type=get_api_key&workspace_id=${props.userInfo?.client_admin_id}`;

    try {
      // setLoading(true)
      const response = await fetch(apiUrl);
      const responseData = await response.json();

      setApiKey(responseData?.data?.api_key);
      // setLoading(false)
    } catch (error) {
      // setLoading(false)
      console.error(error.message);
    }
  };

  const [searchQuery, setSearchQuery] = useState('');

  const handleSearch = (event) => {
    setSearchQuery(event.target.value);
  };

  const [isSearchFieldVisible, setIsSearchFieldVisible] = useState(false);
  const toggleSearchField = (isVisible) => {
    setIsSearchFieldVisible(isVisible);
  };
  const clearSearch = () => {
    setSearchQuery('');
  };

  useEffect(() => {
    fetchApiKey();
  }, []);

  useEffect(() => {
    fetchQrCodes();
  }, []);


  // post api 
  let [displayData, setDisplayData] = useState({});
  const [submitting, setSubmitting] = useState(false);

  let [formData, setFormData] = useState({
    company_id: props.userInfo?.client_admin_id,
    user_id: props.userInfo?.userID,
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

  // const handleOccurrence = async () => {
  //   let response = null;
  //   setLoadingOccurence(true)
  //   // Prepare the data to send to the backend
  //   try {
  //     response = await axios.get(
  //       `https://100105.pythonanywhere.com/api/v3/experience_database_services/?type=get_user_email&product_number=UXLIVINGLAB005&email=${formData.email}`
  //     );
  //     if (response.data.occurrences === 0) {
  //       await axios.post(
  //         `https://100105.pythonanywhere.com/api/v3/experience_database_services/?type=register_user`,
  //         {
  //           product_number: "UXLIVINGLAB005",
  //           email: formData.email,
  //         }
  //       );
  //     }
  //     setLoadingOccurence(false)
  //     setOccurrence(response?.data?.occurrences);
  //     setShowOccurrence(true);
  //     setModalOpen(true);
  //     // console.log("ShowModal", modalOpen)
  //   } catch(e) {
  //       setLoadingOccurence(false)
  //       console.log("Error", e)
  //   }
  // };
  

  const handleFormData = async () => {
    if (formData.link != "") {
      const apiUrl =
      `https://www.uxlive.me/api/qrcode/v1/qr-code/`
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
  }

  const handleSubmit = async (e) => {
    e.preventDefault();
    // handleOccurrence()
    handleFormData()
  };
  
  
  return (

        <>
          
          <div>
            <div class="navBar fixed top-0 left-0 right-0 p-4 mb-6 bg-white flex justify-end items-center">
              {/* Search Icon */}
              <Search
                className="mr-3 flex items-center"
                onClick={() => toggleSearchField(!isSearchFieldVisible)}
                style={{ cursor: 'pointer' }}
              />
  
              <Link 
                href="https://100014.pythonanywhere.com/sign-out"
                class="bg-red-900 hover:bg-red-600 text-white font-semibold py-2 px-4 rounded">
                Logout
              </Link>
            </div>
            
            {
                  isSearchFieldVisible && (
                    <div className={`container w-full md:w-1/4 mx-auto p-4 fixed right-0 ${
                      isSearchFieldVisible ? 'input-fade-in' : 'opacity-0'
                    }`}>
                      <div className="relative">
                        <input
                          type="text"
                          placeholder="Search by Name"
                          value={searchQuery}
                          onChange={handleSearch}
                          className={`w-full px-4 py-2 bg-white border border-gray-300 rounded-xl focus:outline-none  focus:border-green-500`}
                        />
                        {searchQuery && (
                          <button
                            className="absolute right-3 top-2 text-gray-500 cursor-pointer"
                            onClick={clearSearch}
                          >
                            <X />
                          </button>
                        )}
                      </div>
                    </div>
                )
              }

            <div className="flex flex-col justify-center items-center mt-20 rounded-lg overflow-auto">
              <img src="message.svg" alt="Your Name" class="text-center" />
              <h1 className="header text-2xl text-center text-black font-bold">
                Welcome to Dowell URL Shortener <span className="name">{props.userInfo?.first_name}</span>
              </h1>
              <p className="subText text-center">
                Create short and memorable links in seconds
              </p>
            </div>

            <div className="w-screen rounded-lg overflow-auto">
              <div className="container mx-auto p-4 my-2">
                <div className="flex flex-col md:flex-row justify-center items-center space-y-2 md:space-y-0 md:space-x-2">
                  <form onSubmit={handleSubmit}>
                  <div className="flex flex-col md:flex-row w-full space-y-2 md:space-y-0 md:space-x-2">
                    <Input
                      type="text"
                      name="name"
                      value={formData.name || ""}
                      onChange={handleChange}
                      placeholder="Name"
                      className="w-full py-2 bg-white border border-gray-300 rounded-xl focus:outline-none focus:border-green-500"
                    />
                    
                    <Input
                      type="text"
                      name="link"
                      value={formData.link || ""}
                      onChange={handleChange}
                      placeholder="Enter the link here"
                      className="w-full px-4 py-2 bg-white border border-gray-300 rounded-xl focus:outline-none focus:border-green-500"
                    />

                    {/* <Input
                      type="email"
                      name="email"
                      value={formData.email || ""}
                      onChange={handleChange}
                      placeholder="Enter Email"
                      className="w-full px-4 py-2 bg-white border border-gray-300 rounded-xl focus:outline-none focus:border-green-500"
                    /> */}
                    
                    <button
                      disabled={submitting || formData.link === "" || formData.name === ""}
                      type="submit"
                      className="w-full md:w-auto px-4 py-2 btnStyle text-white font-semibold py-2 px-4 rounded flex items-center justify-center"
                    >
                      {submitting ? <Loader2 className="text-4xl animate-spin" /> : 'Submit'}
                    </button>{" "}
                  </div>
                    
                   
                  </form>
                </div>
              </div>
            </div>

            <div className="pb-8 w-screen rounded-lg overflow-auto">
              {
                loading ? <Loader /> : 
                qrcodes?.length > 0 ? 
                <DisplayQRCodes 
                  qrcodes={qrcodes} 
                  apiKey={apiKey}
                  getUserInfo={fetchQrCodes} 
                  searchQuery={searchQuery} 
                  userInfo={props?.userInfo} 
                /> : 
                <NotFound message="No Links Found" />
              }
            </div>

            {showOccurrence && modalOpen && (
              <OccurenceModal
                email={formData?.email}
                showModal={modalOpen}
                setOpenModal={setModalOpen}
                showOccurrence={showOccurrence}
                occurrence={occurrence}
                handleFormData={handleFormData}
              />
            )}
            
          </div>
        </>
  );
};

export default QRCodeForm;
