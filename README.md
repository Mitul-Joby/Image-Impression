# Image-Impression

## Image Compression Using SVD

Compression of images is an incredibly important process which occurs millions of times every day, images by themselves are simply too large to be shared or stored efficiently despite the advancements in storage due to the fact that they are essentially a 2D matrix of bits it’s still too large.


That is the reason people are continuously developing better algorithms for compression of the image as well as maintaining a low loss percentage. This project’s aims are to explore efficient algorithms that can be used for this same process.


## Teammates:

- [Mitul Joby](https://github.com/Mitul-Joby)
- [Navin Srinivas](https://github.com/NavinShrinivas)
- [Mohamed Ayaan](https://github.com/Mohamed-Ayaan358)

## About

In the scope of this project, we applied SVD to images converted to matrices and later dropped trailing singular values to cause “lossy” compression.

<p align="center">
  <img height="256" src="https://user-images.githubusercontent.com/73733877/165220236-bbf25bf0-76c9-427a-9818-a19760ddab69.png">
  &nbsp
  <img height="256" src="https://user-images.githubusercontent.com/73733877/165220248-128b4b8e-639f-4b8b-864d-0d7310091854.png"> 
</p>

## Execution

- `pip install -r requirements.txt`
- Run `compressor.py`

## Results and Discussions

### Images
An initial image of size 142217 Bytes of dimensions 960 x 1280 was passed through the compression algorithm for various values of different number of columns (k). The size of each of the obtained output images are recorded.

|     K      |     COMPRESSION FACTOR    |     SIZE OF COMPRESSED IMAGE (Bytes)    |
|------------|---------------------------|-----------------------------------------|
|     1      |     3.12                  |     45578                               |
|     5      |     2.17                  |     65525                               |
|     10     |     1.84                  |     77284                               |
|     25     |     1.44                  |     98740                               |
|     50     |     1.26                  |     112983                              |
|     75     |     1.15                  |     123735                              |
|     100    |     1.09                  |     129201                              |

<p align="center">
  <img height="512" src="https://user-images.githubusercontent.com/73733877/165221057-72fe691e-9672-4ee1-8f5b-8d067ae910c6.png">
  <br/>
  <br/>
  <img height="256" src="https://user-images.githubusercontent.com/73733877/165220315-53c3819b-38a2-45f7-863a-6d8a4823b37b.png">
</p>

### Square Images
An initial image of size 883866 Bytes of dimensions 2048 x 2048 was passed through the compression algorithm for various values of different number of columns (k). The size of each of the obtained output images are recorded.

|     K      |     COMPRESSION FACTOR    |     SIZE OF COMPRESSED IMAGE (Bytes)    |
|------------|---------------------------|-----------------------------------------|
|     1      |     11.19                 |     78990                               |
|     5      |     8.43                  |     104908                              |
|     10     |     9.53                  |     92684                               |
|     25     |     8.49                  |     104019                              |
|     50     |     7.44                  |     118760                              |
|     75     |     6.08                  |     145386                              |
|     100    |     5.29                  |     167051                              |

<p align="center">
  <img height="512" src="https://user-images.githubusercontent.com/73733877/165221228-2a54a761-72c3-4a7c-b8c4-3619ea920768.png">
  <br/>
  <br/>
  <img height="256" src="https://user-images.githubusercontent.com/73733877/165220379-7e9cd482-0322-4efc-beea-d5a6963fd8c4.png">
</p>



## References

-	https://ieeexplore.ieee.org/abstract/document/1093309
-	https://www.cmi.ac.in/~ksutar/NLA2013/imagecompression.pdf
-	https://web.stanford.edu/class/cme335/lecture6.pdf
- https://web.mit.edu/be.400/www/SVD/Singular_Value_Decomposition.htm
-	Lossy image compression using singular value decomposition and wavelet difference reduction - ScienceDirect
