import { Pagination } from "react-bootstrap"

const Pages =()=>{
    //const PageCount = Math.ceil(servicestore._totalCount/servicestore._limit)
    const PageCount = Math.ceil(10/3)

    const pages = []

    for(let i=0; i<PageCount; i++){
        pages.push(i+1)
    }
    return(
        <Pagination >
            {pages.map(page => 
            <Pagination.Item key={page} /*active={servicestore._page===page} onClick={()=>servicestore.setPage(page)}*/>{page}</Pagination.Item>
            )}
        </Pagination>
    )
    
}

export default Pages