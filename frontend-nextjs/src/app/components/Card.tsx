import { PropsWithChildren } from 'react';


interface CardProps {
title: string;
description?: string;
onClick?: () => void;
}


export default function Card({ title, description, onClick }: PropsWithChildren<CardProps>) {
return (
    <div onClick={onClick} className="p-6 bg-white rounded-2xl shadow-sm hover:shadow-lg transition cursor-pointer border border-gray-100">
        <h3 className="text-xl font-semibold mb-2">{title}</h3>
        {description && <p className="text-gray-600 text-sm">{description}</p>}
    </div>
);
}