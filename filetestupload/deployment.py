class Deployment:
    def request(self, data):

        data = data["input"]

        output_1 =  {
            "file": data,
            "bucket_file": "file/path/1.txt"
        }
        output_2 =  {
            "file": data,
            "bucket_file": "file/path/2.txt"
        }
        return {"output" : [output_1, output_2]}
