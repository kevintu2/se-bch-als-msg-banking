import {Form} from 'react-bootstrap';

function Upload() {
    return (
        <div>
            <Form.Group controlId="formFile" className="mb-3">
                <Form.Label>Upload your data</Form.Label>
                <Form.Control type="file" />
            </Form.Group>
        </div>
    );
}

export default Upload;