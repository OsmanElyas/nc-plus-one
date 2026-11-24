import { useEffect, useState } from "react"
import { type Event } from "../../types/event";
import { listEvents } from "../api/events";

export function useEvents(){
    const [events, setEvents] = useState<Event[]>([]);
    const [isLoading, setIsLoading] = useState(true);
    const [error, setError] = useState<string | null>(null);

    useEffect(() =>{
        const fetchEvents = async () => {
            setIsLoading(true);
            setError(null);

            try{
                const response = await listEvents();
                setEvents(response);


            }catch{
                setError("Something went wrong")
            }finally{
                setIsLoading(false)
            }
        };
        fetchEvents();
    },[])

    return {events, isLoading, error};
}