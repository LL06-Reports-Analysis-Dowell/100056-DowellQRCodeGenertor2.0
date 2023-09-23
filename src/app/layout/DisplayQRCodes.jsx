/* eslint-disable @next/next/no-img-element */
"use client";
import React, { useEffect, useState } from "react";
import { QrCode, Pencil, Copy } from "lucide-react";
import { Button } from "@/components/ui/button";
import * as DialogPrimitive from "@radix-ui/react-dialog";
import EditComponent from './EditComponent'
import { toast } from "react-toastify";


import {
  Dialog,
  DialogContent,
  DialogDescription,
  DialogHeader,
  DialogTitle,
  DialogTrigger,
} from "@/components/ui/dialog";


const DisplayQRCodes = (props) => {
  const copylink = (e) => {
    const link = e.currentTarget.getAttribute("link");

    navigator.clipboard.writeText(link);
    toast.info("Link Copied")
  };

  return (
    <div className="md:mr-10 md:ml-10">
      {props.qrcodes.map((qrcode, key) => {
        return (
          <div
            key={key}
            className="pb-4 rounded-xl p-3 cardbg  m-4  sm:flex sm:flex-col md:grid md:grid-cols-4 text-white"
          >
            <div className="mr-3 mb-3 md:mb-0 md:mr-0">
              <p className="urlText text-xs">Name</p>
              <p className="shortenUrl">{qrcode?.name}</p>
            </div>

            <div className="mr-3 mb-3 md:mb-0 md:mr-0">
              <p className="urlText text-xs">Original URL</p>
              <a href={qrcode?.link_} className="shortenUrl">{qrcode?.link_}</a>
            </div>
            
            <div className="mr-3 mb-3 mr:mr-0">
              <p className="urlText text-xs">Shorten URL</p>
              <a href={qrcode?.link} className="shortenUrl">{qrcode?.link}</a>
            </div>
            
            <div className="flex md:justify-end sm:justify-start items-center">
              {/* qr  modal button  */}
              <Dialog>
                <DialogTrigger>
                  <QrCode className="icon"/>
                </DialogTrigger>
                <DialogContent className="text-white modalBg ">
                  <DialogHeader>
                    <DialogTitle>
                      Scan Qrcode
                    </DialogTitle>
                    <DialogDescription>
                        <img
                          src={qrcode?.qrcode_image_url}
                          width="auto"
                          height="auto"
                          alt="qr image to scan"
                          className="mx-auto"
                        />
                      {/* <a href={qrcode.qrcode_image_url} className="shortenUrl text-white-400 text-md">
                        {qrcode.qrcode_image_url}
                      </a> */}
                      <div className="flex justify-center gap-x-5 text-center my-5">
                        <DialogPrimitive.Close>
                          <Button className="greyBtn text-white font-bold rounded-md p-5">
                            Cancel
                          </Button>
                        </DialogPrimitive.Close>
                        <Button
                          link={qrcode.qrcode_image_url}
                          className="greenBtn text-white font-bold rounded-md p-5"
                          onClick={copylink}
                        >
                          Copy Qrcode Image Link
                        </Button>
                      </div>
                    </DialogDescription>
                  </DialogHeader>
                </DialogContent>
              </Dialog>


              <div className="icon ml-3">
                <EditComponent qrcode={qrcode} infoFucntion={props.getUserInfo}/>
              </div>
              <button className="icon ml-3" link={qrcode.link} variant="outline" onClick={copylink}>
                <Copy />
              </button>
            </div>
          </div>
        );
      })}
    </div>
  );
};

export default DisplayQRCodes;
