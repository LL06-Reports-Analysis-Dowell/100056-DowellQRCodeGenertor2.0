'use client'
import React, { useEffect } from 'react'
import {Pencil, Send} from 'lucide-react'
import * as DialogPrimitive from "@radix-ui/react-dialog";
import { Button } from "@/components/ui/button";
import { useState } from 'react';
import { toast } from "react-toastify";
import { Loader2 } from "lucide-react"
import { TextInput } from "@/components/ui/textInput"

import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
  } from "@/components/ui/dialog";
  
const SendEmailComponent = (props) => {
    
  // put api function
  const [sending, setSending] = useState(false);
  

  let [formData, setFormData] = useState({
    fromName: "Dowell UX Living Lab",
    fromEmail: "dowell@dowellresearch.uk",
    email: "",
    name: "",
    subject: "Link Shortener",
    body: "This link will take you to a page where you access the information you need. You can also scan the Qrcode attached.",
    api_key: props?.apiKey,
    qrcode_image_url: props?.qrcode?.qrcode_image_url,
  });

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prevData) => ({
      ...prevData,
      [name]: value,
    }));
  };

  

  const handleSubmit = async (e) => {
    const id = e.currentTarget.getAttribute("qrcode_ID");
    
    const apiUrl = `https://100085.pythonanywhere.com/api/v1/mail/${formData.api_key}/?type=send-email`;
    const requestData = {
      fromName: formData?.fromName,
      fromEmail: formData?.fromEmail,
      name: formData?.name,
      email: formData?.email,
      api_key: formData?.api_key,
      subject: formData?.subject,
      body: formData?.body
    };

    const htmlContent = `
        <!DOCTYPE html>
        <html lang="en">
        <head>
        <meta charset="UTF-8">
        <title>Email Template</title>
        </head>
        <body>
            <div style="color: #000000;">${requestData?.body}</div>
            <a href=${props?.qrcode?.link}>${props?.qrcode?.link}</a><br>
            <img style="width: 250px; height: auto;" src=${formData?.qrcode_image_url} alt="Attached Qrcode Image" />
        </body>
        </html>
    `;
    requestData.body = htmlContent;
    console.log("data", requestData);
    try {
      setSending(true);
      const response = await fetch(apiUrl, {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      const responseData = await response.json();
      console.log("API response PUT:", responseData); 

      if(responseData.success == true){
        setSending(false);
        toast.success(`${responseData?.message}. ${responseData?.credits} credits remaining.`)
        // props.infoFucntion();
      }   

      if(responseData.success == false){
        setSending(false);
        toast.error(responseData?.message);
      }
    } catch (error) {
      setSending(false);
      console.log(error);
    }
  };

  
  

  return (
    <div>
       <Dialog>
        <DialogTrigger>
          <Send />
        </DialogTrigger>

        <DialogContent className="modalBg">
          <DialogHeader>
            <DialogTitle className="edit text-md mb-3 font-bold">
              Share Link
            </DialogTitle>

            <DialogDescription>
              {/* <div className='mb-2'>
                <label
                  for="fromName"
                  class="block edit text-white text-sm font-bold mb-1"
                >
                  From
                </label>
                <TextInput
                  name="fromName"
                  type="text"
                  value={formData.fromName}
                  readonly
                  placeholder="Enter Your Name"
                />
              </div>
               */}
              {/* <div className="mb-2">
                <TextInput
                  name="fromEmail"
                  type="fromEmail"
                  placeholder="Enter Your Email"
                  readonly
                  value={formData.fromEmail}
                />
              </div> */}

              <div className="mb-2">
                <label
                  for="name"
                  class="block edit text-sm font-bold mb-1"
                >
                  To
                </label>
                <TextInput
                  name="name"
                  placeholder='Enter Recepient Name'
                  type="text"
                  value={formData.name || ""}
                  onChange={handleChange}
                />
              </div>

              <div className="mb-2">
                <TextInput
                  name="email"
                  type="email"
                  placeholder='Enter Recepient Email'
                  value={formData.email}
                  onChange={handleChange}
                />
              </div>

              {/* <div className="mb-2">
                <p className="text-xs text-gray-500 mt-1 ml-1">Email Subject</p>
                <TextInput
                  name="subject"
                  type="subject"
                  placeholder='Email Subject'
                  value={formData.subject}
                  onChange={handleChange}
                />
              </div> */}

              <div className="mb-2">
                <p className="text-xs text-gray-500 mt-2 ml-1">Email Body</p>
                <textarea
                  name="body"
                  type="body"
                  id="body"
                  placeholder='Body'
                  value={formData.body || ""}
                  onChange={handleChange}
                  className='text-black w-full h-32 p-4 border border-gray-300 rounded-xl focus:outline-none  focus:border-green-500 resize-y align-top'
                />
                <p className="text-xs text-gray-400 mt-1 ml-3">
                  Note: The Qrcode and shortened Link are attached to the email. Feel free Personalize the Email Body to your satisfaction.
                </p>
              </div>

                
              <div className="flex justify-center gap-x-5 text-center my-5">
                <DialogPrimitive.Close>
                  <Button className="w-full md:w-auto px-4 py-2 text-black focus:outline-none  flex items-center justify-center">
                    Cancel
                  </Button>
                </DialogPrimitive.Close>
                <button
                  qrcode_ID={props.qrcode.qrcode_id}
                  className="w-full md:w-auto px-4 py-2 btnStyle text-white font-semibold py-2 px-4 rounded flex items-center justify-center"
                  type="button"
                  onClick={handleSubmit}
                  disabled={sending || formData.api_key === "" || formData.name === "" || formData.email === ""}
                >
                  {sending ? <Loader2 className="mr-2 h-4 w-4 text-4xl animate-spin" /> : 'Share'}
                </button>
              </div>
            </DialogDescription>
          </DialogHeader>
        </DialogContent>
      </Dialog>
    </div>
  )
}

export default SendEmailComponent
