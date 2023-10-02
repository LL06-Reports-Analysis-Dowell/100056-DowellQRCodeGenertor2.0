import React from 'react'

export const TextInput = (props) => {
  return (
    <input
        readonly={props?.readonly}
        name={props?.name}
        type={props?.text}
        value={props?.value}
        onChange={props?.onChange}
        placeholder={props?.placeholder}
        className={`text-black w-full px-3 py-2 border border-gray-300 rounded-xl focus:outline-none ${props.readonly ? "cursor-not-allowed pointer-events-none focus:outline-none" : "focus:border-green-500"}`}
    />
  )
}



export const TextArea = () => {
  return (
    <div>textInput</div>
  )
}

