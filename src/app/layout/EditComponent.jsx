'use client'
import React from 'react'
import {Pencil} from 'lucide-react'
import * as DialogPrimitive from "@radix-ui/react-dialog";
import { Button } from "@/components/ui/button";
import { useState } from 'react';
import { toast } from "react-toastify";
import { Loader2 } from "lucide-react"


import {
    Dialog,
    DialogContent,
    DialogDescription,
    DialogHeader,
    DialogTitle,
    DialogTrigger,
  } from "@/components/ui/dialog";
import { TextInput } from '@/components/ui/textInput';
  
const EditComponent = (props) => {
    
  // put api function
  const [editing, setEditing] = useState(false);

  let [formData, setFormData] = useState({
    link: props.qrcode?.link_,
    name:  props.qrcode?.name,
    word_1: props.qrcode?.word,
    word_2: props.qrcode?.word2,
    word_3: props.qrcode?.word3,
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
    
    const apiUrl = `https://www.uxlive.me/api/qrcode/v1/update-qr-code/${id}`;
    const requestData = {
      link: formData.link,
      name: formData?.name,
      word: formData.word_1,
      word2: formData.word_2,
      word3: formData.word_3,
    };
    console.log("data", requestData);
    try {
      setEditing(true);
      const response = await fetch(apiUrl, {
        method: "PUT",

        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(requestData),
      });

      const responseData = await response.json();
      console.log("API response PUT:", responseData); 
      if(responseData.success){
        setEditing(false);
        toast.success(responseData?.success)
        props.infoFucntion();
      }   
      if(responseData.error){
        setEditing(false);
        toast.error(responseData?.error);
      }
    } catch (error) {
      setEditing(false);
      console.error(error.message);
    }
  };

  return (
    <div>
       <Dialog>
        <DialogTrigger>
          <Pencil />
        </DialogTrigger>
        <DialogContent className="modalBg">
          <DialogHeader>
            <DialogTitle className="edit text-md mb-3 font-bold">
              Edit URL
            </DialogTitle>
            <DialogDescription>
              <div className="mb-2">
                <label
                  for="link"
                  class="block edit text-sm mb-1"
                >
                  Link
                </label>
                <TextInput
                  name="link"
                  type="text"
                  value={formData.link}
                  onChange={handleChange}
                  placeholder="Enter the link here"
                />
              </div>

              <div className="mb-2">
                <label
                  for="name"
                  class="block edit text-sm mb-1"
                >
                  Name
                </label>
                <TextInput
                  name="name"
                  type="text"
                  value={formData.name}
                  onChange={handleChange}
                  placeholder="Enter the name here"
                />
              </div>

              <div className="mb-2">
                <label
                  for="link"
                  class="block edit text-sm mb-1"
                >
                  Master Link
                </label>
                <div className="grid grid-cols-4 gap-x-2">
                  <input
                    type="text"
                    placeholder="Readonly Input"
                    className="w-full bg-transparent edit h-10 px-0 border border-transparent rounded-md focus:outline-none focus:none focus:none"
                    readonly
                    value="https://www.qrcodereviews.uxlivinglab.online/"
                  />
                  {/* {props.qrcode.link} */}

                  <TextInput
                    name="word_1"
                    value={formData.word_1}
                    onChange={handleChange}
                    type="text"
                    placeholder="word1"
                  />

                  <TextInput
                    name="word_2"
                    value={formData.word_2}
                    onChange={handleChange}
                    type="text"
                    placeholder="word2"
                  />

                  <TextInput
                    name="word_3"
                    value={formData.word_3}
                    onChange={handleChange}
                    type="text"
                    placeholder="word3"
                  />
                </div>
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
                  disabled={editing}
                >
                  {editing ? <Loader2 className="mr-2 h-4 w-4 text-4xl animate-spin" /> : 'Update URL'}
                </button>
              </div>
            </DialogDescription>
          </DialogHeader>
        </DialogContent>
      </Dialog>
    </div>
  )
}

export default EditComponent
