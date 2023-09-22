"use client";
import React, { useEffect, useState } from "react";
import { QrCode, Pencil, Copy } from "lucide-react";
import { useToast } from "@/components/ui/use-toast";
import { Button } from "@/components/ui/button";
import * as DialogPrimitive from "@radix-ui/react-dialog";
import EditCompoenet from './EditCompoenet'

import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";
import { Loader } from "./Loader";

const DisplayQRCodes = () => {
  const [qrcodes, setQRCodes] = useState();
  const { toast } = useToast();

  const userId = sessionStorage.getItem("userId");
  const getUserInfo = async () => {
    console.log("fetching");

    const apiUrl = `https://www.qrcodereviews.uxlivinglab.online/api/v4/qr-code/?user_id=${userId}`;

    try {
      const response = await fetch(apiUrl);

      if (response.status !== 200) {
        alert("timed out");
        toast({
          title: "error timed out",
          description: "Friday, February 10, 2023 at 5:57 PM",
        });
      }
      const responseData = await response.json();
      console.log("status", responseData.status);
      await setQRCodes(responseData.response.data);
      console.log("API response GET:", responseData);
      if (responseData.response.length == 0) {
        alert("Qr code does not exist with this id");
      } else {
        console.log("DD", responseData);
      }
    } catch (error) {
      console.error(error.message);
    }
  };
  console.log("qrcode", qrcodes);

  useEffect(() => {
    getUserInfo();
  }, [userId]);

  const copylink = (e) => {
    const link = e.currentTarget.getAttribute("link");

    navigator.clipboard.writeText(link);
    toast({
      title: `Link Coppied`,
      description: `${link}`,
      className: "text-white btnStyle border-none]",
    });
  };

  return (
    <div>
      {qrcodes? qrcodes.map((qrcode, key) => {
        return (
          <div
            key={key}
            className="pb-4 rounded-xl p-3 cardbg gap-y-6 gap-x-4 m-4 grid grid-cols-3 text-white"
          >
            <div>
              <p className="urlText text-xs">Original URL</p>
              <p className="shortenUrl">{qrcode.link_}</p>
            </div>
            <div>
              <p className="urlText text-xs">Shorten URL</p>
              <p className="shortenUrl">{qrcode.link}</p>
            </div>
            <div className="flex justify-between items-center gap-x-5">
              {/* qr  modal button  */}
              <Dialog className="text-white">
                <DialogTrigger>
                  <QrCode />
                </DialogTrigger>
                <DialogContent className="text-white modalBg ">
                  <DialogHeader>
                    <DialogTitle>
                      <img
                        src={qrcode.qrcode_image_url}
                        width="200px"
                        height="300px"
                        alt="qr image to scan"
                        className="mx-auto"
                      />
                    </DialogTitle>
                    <DialogDescription>
                      <p className="text-green-400 text-md font-bold text-center whitespace-normal overflow-ellipsis">
                        {qrcode.qrcode_image_url}
                      </p>
                      <div className="flex justify-center gap-x-5 text-center my-5">
                        <DialogPrimitive.Close>
                          <Button className="greyBtn text-white font-bold rounded-md p-5">
                            Cancel
                          </Button>
                        </DialogPrimitive.Close>
                        <Button
                          link={qrcode.qrcode_image_url}
                          className=" greenBtn text-white font-bold rounded-md p-5"
                          onClick={copylink}
                        >
                          Copy Link
                        </Button>
                      </div>
                    </DialogDescription>
                  </DialogHeader>
                </DialogContent>
              </Dialog>

              {/* edit qrcode  */}

             <EditCompoenet qrcode={qrcode} infoFucntion={getUserInfo}/>

              {/* copy link  */}
              <button link={qrcode.link} variant="outline" onClick={copylink}>
                <Copy />
              </button>
            </div>
          </div>
        );
      }):<Loader/>}
    </div>
  );
};

export default DisplayQRCodes;
